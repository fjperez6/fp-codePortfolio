{Francisco Perez	7/24/2013							}
{CSC540 - 13SU - Graduate Research Seminar - Summer					}
{											}
{This program makes use of a series of commented loops to simulate a game of roulette.  }
{the principal loop runs according to user input. Matching statements will then         }
{increment a particular counter to answer the assignment's 3 questions.			}
{This program uses no external input or output file.					}
{Compiled and tested with: 'Free Pascal Compiler version 2.6.0-6 [2012/10/05] for i386'	}

program roulette;

const
	numSlot				= 37;  {roulette slots 0 - 36}
	particularNumber		= 13;  {search value for question 'B'}

var 
	numSpins, j			: qword;
	twoXinaRow			: int64;
	threeXinaRow			: int64;
	previousSpinValue		: integer;
	prevPreviousSpinValue		: integer;
	particularNumberFound		: Boolean;
	numConsecutiveEvenOddSpins	: int64;
	numMostConsecutiveEvenSpins	: int64;
	numMostConsecutiveOddSpins	: int64;
	currentSpinValue		: integer;
	particularNumberFoundonSpin	: int64;

begin
	j				:= 0;  {used as loop counter}
	twoXinaRow			:= 0;  {variable to count two matching numbers in a row}
	threeXinaRow			:= 0;  {variable to count three matching numbers in a row}
	previousSpinValue		:= 40;  {set a value that will not match any first throw}
	prevPreviousSpinValue		:= 40;  {set a value that will not match any first throw}
	particularNumberFound		:= False;  {Indicates if the particular num from question 'B' is found}
	numConsecutiveEvenOddSpins	:= 1;
	numMostConsecutiveEvenSpins	:= 1;
	numMostConsecutiveOddSpins	:= 1;
	
	write('How many spins would you like to do? ');
	readln(numSpins);  {user input for number of spins}
	
	randomize;
	
	writeln;
	writeln('Your simulation is running');

	while (j < numSpins) do  {Loops until reaching user input number of spins}
	begin
		j := j + 1;  {increment loop counter}
		currentSpinValue := random(numSlot);  {generates random number between 0 - 36}

		if (currentSpinValue = previousSpinValue) then  {matches for spin values in a row}
		begin 
			twoXinaRow := twoXinaRow + 1;  {increments counter for question 'A' part 1}	
			if (currentSpinValue = particularNumber) AND (particularNumberFound = False) then  {Matches for number in Question 'B'}
			begin 
				particularNumberFoundonSpin := j;  {records the spin that number for Question 'B'}	
				particularNumberFound := True;  {sets indication for program to stop looking for number for Question 'B'}
			end;
			if (previousSpinValue = prevPreviousSpinValue) then {matches 1st previous spin to second previous spin for Question 'A'}
				threeXinaRow := threeXinaRow + 1;	{increments counter for question 'A' part 2}
		end; {end: matches for spin values in a row}
		{find run of even/odd in a row}
        if (currentSpinValue = 0) then  {Matches for spin value of '0' to reset counter of consecutive even}
		    numConsecutiveEvenOddSpins := 1;	
		if (j > 1) AND (currentSpinValue <> 0) AND (currentSpinValue MOD 2 = 0) AND (previousSpinValue MOD 2 = 0) then
		begin  {Matches for consecutive even spins in arrow. Starting at spin 2 to avoid counting preset 'previousSpinValue's}
                {aviods matching for '0'}
			numConsecutiveEvenOddSpins := numConsecutiveEvenOddSpins + 1;	{increments counter for question 'C' part 1}
			if (numConsecutiveEvenOddSpins > numMostConsecutiveEvenSpins) then
				numMostConsecutiveEvenSpins := numConsecutiveEvenOddSpins;  {keeps record of longest run of even values} 
		end;
		if (currentSpinValue MOD 2 = 0) AND (previousSpinValue MOD 2 = 1) then  {resets counter of consecutive even}
			numConsecutiveEvenOddSpins := 1;	
		if (currentSpinValue MOD 2 = 1) AND (previousSpinValue MOD 2 = 1) then  {Matches for consecutive odd spins in a row} 
		begin
			numConsecutiveEvenOddSpins := numConsecutiveEvenOddSpins + 1;	{increments counter for question 'C' part 2}
			if (numConsecutiveEvenOddSpins > numMostConsecutiveOddSpins) then
				numMostConsecutiveOddSpins := numConsecutiveEvenOddSpins;  {keeps record of longest run of odd values} 
		end;
		if (currentSpinValue MOD 2 = 1) AND (previousSpinValue MOD 2 = 0) then  {resets counter of consecutive odd}
			numConsecutiveEvenOddSpins := 1;	
	   {end: find run of even/odd in a row}

		prevPreviousSpinValue := previousSpinValue;
		previousSpinValue := currentSpinValue;
	end; {while spin loop}
 
	{output section}
	writeln;
	writeln('Question A');
	writeln('On average, a Number comes up two times in a row:');
	writeln(100*(twoXinaRow/numSpins):6:3, '%');  {calculates average for any number appearing twice in a row}
	writeln('On average, a Number comes up three times in a row:');
	writeln(100*(threeXinaRow/numSpins):6:3, '%');  {calculates average for any number appearing thrice in a row}
	writeln;
	writeln('Question B');
	if (particularNumberFound = False) then
		writeln('The particular number: ', particularNumber, ' did not appear twice in a row')
	else
		writeln('The particular number: ', particularNumber, ' came up twice in a row on spin ', particularNumberFoundonSpin);
	writeln;
	writeln('Question C');
	writeln('The longest run of evens in a row is: ', numMostConsecutiveEvenSpins);
	writeln('The longest run of odds in a row is: ', numMostConsecutiveOddSpins);
	writeln;

	{push 'ENTER' to Exit program. Necessary if run from IDE to prevent window from disappearing}
	write('Push ENTER to finish the program.');
	readln;
end.
