#!/usr/bin/perl -w
use strict;
use Tk;
use Tk::DateEntry;
use Tk::ROText;
use Text::CSV;
use IO::File;
use DBI qw(:sql_types);
use POSIX qw(strftime);
use Time::Local;

# Variables
my $filepath;
our %idx_for_mon = ( JAN=>"01", FEB=>"02", MAR=>"03", APR=>"04", MAY=>"05", JUN=>"06"
		 		,JUL=>"07", AUG=>"08", SEP=>"09", OCT=>"10", NOV=>"11", DEC=>"12" );

my $curr_day	= strftime("%d", localtime);
my $curr_mon	= strftime("%m", localtime);
my $curr_year	= strftime("%Y", localtime);
my $input		= &format("$curr_year", "$curr_mon", "$curr_day");

#build GUI interface
my $mw 			= MainWindow->new;
$mw->geometry( '400x300' );
$mw->resizable( 0, 0 );

my $menu_f 		= $mw->Frame()->pack(
					-side=>'top',
					-fill=>'x');

my $menu_file 	= $menu_f->Menubutton (
					-text=>'File',
					-tearoff=>'false')->pack(
					-side=>'left');

$menu_file->command(-label=>'Update',
            		-command=> \&file_get); 

my $date_label 	= $mw->Label(
					-text=>"Search by Date:",
					-width=>20, )->pack;

my $date_entry 	= $mw->DateEntry(
					-textvariable=>\$input,
					-width=>11,
			 		-parsecmd=>\&parse,
					-formatcmd=>\&format,
					-todaybackground=>"green", )->pack;

my $last_name_label = $mw->Label(
					-text=>"Search by First Name:",
					-width=>20, )->pack;

my $last_name_entry = $mw->Entry(
					-width=>11, )->pack;

my $first_name_label = $mw->Label(
					-text=>"Search by Last Name:",
					-width=>20, )->pack;

my $first_name_entry = $mw->Entry(
					-width=>11, )->pack;

my $order_num_label = $mw->Label(
					-text=>"Search by Order# :",
					-width=>20, )->pack;

my $order_num_entry = $mw->Entry(
					-width=>8, )->pack;

$mw->Button(
					-text=>'Report',
	     			-command=>sub{ report_output( $input, ) } )->pack(
					-side=>'left' );
	
$mw->Button(
					-text=>'Quit',
					-command=>sub{ exit } )->pack(
					-side=>'right' );

MainLoop;
# called on to format date for querying database 
sub parse {
	my ( $day, $mon, $yr ) = split '-', $_[0];
	return ( $yr, $idx_for_mon{ $mon }, $day );
}

# called on to format the date in date entry widget  
sub format {
	my ( $yr, $mon, $day ) = @_;
	$mon = sprintf("%02d", $mon);
	my %mon_for_idx = reverse %idx_for_mon;
	return sprintf( "%02d-%s-%2d", $day, $mon_for_idx{ $mon }, $yr );
}

#manages the output report to toplevel window
sub report_output {
	my ( $input ) = shift;
    my ( $yr, $mon, $day, $output );
#if search date is entered, date variable must be formatted 'YYYY-MM-DD'
#before sending to query database
	if (defined $input && length $input > 0) {
		my ( $yr, $mon, $day ) = parse( $input );
		$output	= query_db( 
				ORDER_DATE => "$yr-$mon-$day",
				CUST_FIRST_NAME => $last_name_entry -> get(),
				CUST_LAST_NAME => $first_name_entry -> get(),
				ORDER_NUM => $order_num_entry -> get(),
				 );
	}
#Otherwise Query is done without the date specified
	else {
		$output	= query_db( 
				CUST_FIRST_NAME => $last_name_entry -> get(),
				CUST_LAST_NAME => $first_name_entry -> get(),
				ORDER_NUM => $order_num_entry -> get(),
				 );
	}
#Creates Topleve window after clicking 'report' button 
	if (! Exists(my $tl)) {
		my $tl = $mw->Toplevel;
		$tl->title("Daily Report");
		$tl->label("Report for " . $input);
		$tl->Button(
			-text => 'Close',
			-command => sub { $tl->withdraw })->pack( -side=>'bottom' );

		my $text = $tl->Scrolled(
			'ROText',
			-scrollbars => 'osoe',
			-wrap       => 'word',
			-width      => 90,
			-height     => 32,
			-setgrid    => 1,)->pack(
				-expand => 1,
					-fill => 'both');
#data is returned from query_db sub and formatted to Toplevel window
#TODO: Create external file for saving queries. Would help with formatting issues
#as well as accessibility
       	$text->insert('end', "Date\t\t   Last Name\t\tfirst name\t\tItem Name\tsale#\n");
		foreach my $row (@$output) {
        	my ($date, $cust_id, $first_name, $last_name, $order_id
			, $item_name, $item_mfgr, $item_price) = @$row;
        	$text->insert('end', "$date $last_name\t\t$first_name\t\t$item_name\t$order_id\n");
    	}
	}
	else {
		$tl->deiconify;
		$tl->raise;
	}
}

# called on to get csv file as part of the menu drop-down widget
sub file_get {
	my @types = (
		["CSV files", [qw/.csv .CSV/]],
        ["All files",        '*']);

	$filepath = $mw->getOpenFile(-filetypes => \@types) or return();
#sends selected file to database input subroutine
	parse_csv($filepath);
}

#parses selected csv 
sub parse_csv {
	my $file = shift;
	my @records;
	my $fh = new IO::File;
	$fh->open("$file", "r");
	my $csv = Text::CSV->new ({ allow_whitespace => 1 })
			or die "Cannot use CSV: ".Text::CSV->error_diag ();
#creates hash with csv header (first line) as keys
	$csv->column_names ($csv->getline ($fh));
#insert remaining csv rows as values in hash
	while ( my $hr = $csv->getline_hr($fh)){
		push @records, $hr;
	}
	close $fh;
#send hash of csv file to update the db
	update_db(@records);
}

#Create Database Tables
sub update_db {
	my @rows = @_;
	my $sql_AddOrder_DTL= qq{ INSERT INTO Orders_DTL VALUES ( ?, ?, ?, ?, ?, ?, ?, ? ) };

#Attempt to connect to database else create sales.db
	my $dbh				= DBI->connect(          
						"dbi:SQLite:dbname=sales.db", 
						"",                          
						"",                          
						{ RaiseError => 1 },) or die $DBI::errstr;
#Create table for the database
#TODO:Normalize db 
	eval {
		$dbh->do("CREATE TABLE IF NOT EXISTS Orders_DTL(order_date TEXT, customer_id INTEGER
			 	, customer_first_name TEXT, customer_last_name TEXT, order_id TEXT, item_name TEXT
				, item_mfgr TEXT, item_price TEXT)");
	};
	
	my $sth_AddOrder_DTL= $dbh->prepare( $sql_AddOrder_DTL );
#bind values from csv hash to sqlite operation
	for my $i (0 .. $#rows) {
		eval {
			$sth_AddOrder_DTL->bind_param( 1, $rows[$i]{'order date'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->bind_param( 2, $rows[$i]{'customer id'}, SQL_INTEGER );
			$sth_AddOrder_DTL->bind_param( 3, $rows[$i]{'customer first_name'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->bind_param( 4, $rows[$i]{'customer last_name'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->bind_param( 5, $rows[$i]{'order number'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->bind_param( 6, $rows[$i]{'item name'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->bind_param( 7, $rows[$i]{'item manufacturer'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->bind_param( 8, $rows[$i]{'item price'}, SQL_VARCHAR );
			$sth_AddOrder_DTL->execute();
		}
	}
 
	$sth_AddOrder_DTL->finish();
	$dbh->disconnect();
}

#query db from the values main window widgets
sub query_db {
	my %args = @_;
    my @clauses;
	my @bind;

#build search clauses based on arguments passed to the subroutine
#first name and last name queries are converted to uppercase to make
#it simpler to search. 
	if ($args{CUST_FIRST_NAME})	{push @clauses, "upper(customer_first_name) LIKE ?";
								 push @bind, uc $args{CUST_FIRST_NAME}}
	if ($args{CUST_LAST_NAME})	{push @clauses, "upper(customer_last_name) LIKE ?";
								 push @bind, uc $args{CUST_LAST_NAME}}
	if ($args{ORDER_NUM})		{push @clauses, "order_id = ?";
								 push @bind, $args{ORDER_NUM}}
	if ($args{ORDER_DATE})		{push @clauses, "order_date LIKE ?";
								 push @bind, "$args{ORDER_DATE}%"}
	my $clause = join(" AND ", @clauses);

#create the query string to be passed to db object
	my $sql     = qq{ SELECT * FROM Orders_DTL WHERE $clause };

#connect to sales.db
    my $dbh             = DBI->connect(          
                        "dbi:SQLite:dbname=sales.db", 
                        "",                          
                        "",                          
                        { RaiseError => 1 },) or die $DBI::errstr;

#execute query on db object
    my $sth     = $dbh->prepare( $sql );
	$sth->execute(@bind);

#stores query output in hash reference for managing report output 
	my $rows_output = $sth->fetchall_arrayref();

    $sth->finish();
    $dbh->disconnect();
#send query back to report output sub
	return $rows_output;
}
