-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1) search the crime scene report on the Humphrey Street at that day
SELECT description, month, day, year  FROM crime_scene_reports
 WHERE street LIKE '%Humphrey Street%';

       -- REPORT: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
       --         Interviews were conducted today with three witnesses who were present at the time –
       --         each of their interview transcripts mentions the bakery.

-- 2) search in the interviews for bakery mentions, to see who are present on the crime scene
SELECT transcript, name FROM interviews
 WHERE transcript LIKE '%bakery%';

        --| Ruth:     Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
        --              If you have security footage from the bakery parking lot, you might want to look for cars that left the parking
        --              lot in that time frame.

        --| Eugene:   I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's
        --              bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

        --| Raymond:  As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
        --              I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief
        --              then asked the person on the other end of the phone to purchase the flight ticket.

        --| Emma:     I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour.
        --              They never bought anything.


-- 3) search name of the people by their car plates, JOINING people with bakery_security_logs column's
 SELECT name FROM people
   JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
  WHERE month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute BETWEEN 15 AND 30
    AND activity = 'exit';

            --+---------+
            --|  name   |
            --+---------+
            --| Vanessa |
            --| Bruce   |
            --| Barry   |
            --| Luca    |
            --| Sofia   |
            --| Iman    |
            --| Diana   |
            --| Kelsey  |
            --+---------+
            -- All are susects

-- 4) search names that used their accounts that day on Leggett Street, JOINING person with bank_accounts and atm_traansactions
SELECT name FROM people
  JOIN bank_accounts ON bank_accounts.person_id = people.id
  JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
 WHERE year = 2021 AND month = 7 AND day = 28
   AND atm_location LIKE '%Leggett Street%';

            --+---------+
            --|  name   |
            --+---------+
            --| Bruce   |
            --| Kaelyn  |
            --| Diana   |
            --| Brooke  |
            --| Kenny   |
            --| Iman    |
            --| Luca    |
            --| Taylor  |
            --| Benista |
            --+---------+
            -- The suspects are:
            --| Bruce   |
            --| Luca    |
            --| Iman    |
            --| Diana   |

-- SELECT the name of passengers on the first flight at 07/29/2021
SELECT name FROM people
  JOIN passengers ON passengers.passport_number = people.passport_number
 WHERE passengers.flight_id = (
       SELECT id FROM flights
        WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
		SELECT id FROM airports
		 WHERE city LIKE 'fiftyville')
     ORDER BY hour ASC, minute ASC
	LIMIT 1);

              --+--------+
              --|  name  |
              --+--------+
              --| Doris  |
              --| Sofia  |
              --| Bruce  |
              --| Edward |
              --| Kelsey |
              --| Taylor |
              --| Kenny  |
              --| Luca   |
              --+--------+
              -- The suspects are:
              --| Bruce   |
              --| Luca    |

-- 5) discover who is the thief
  SELECT people.name FROM people
    JOIN phone_calls ON phone_calls.caller = people.phone_number
   WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60
     AND people.name IN (
				SELECT name FROM people
				  JOIN passengers ON passengers.passport_number = people.passport_number
				 WHERE passengers.flight_id = (
				       SELECT id FROM flights
        				WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
						          SELECT id FROM airports
		 				          WHERE city LIKE 'fiftyville')
     				 ORDER BY hour ASC, minute ASC LIMIT 1))
     AND people.name IN (
				 SELECT name FROM people
				   JOIN bank_accounts ON bank_accounts.person_id = people.id
  				 JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
 				  WHERE year = 2021 AND month = 7 AND day = 28
   				  AND atm_location LIKE '%Leggett Street%')
     AND people.name IN (
				 SELECT name FROM people
  				 JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
				  WHERE month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute BETWEEN 15 AND 30
				  AND activity = 'exit'
)
ORDER BY phone_calls.duration ASC;

                --+-------+
                --| name  |
               ---+-------+
-- The THIEF is:  | Bruce |
                --+-------+

-- 6) discover the thief's destination city
SELECT city FROM airports
 WHERE id = (
         SELECT destination_airport_id FROM flights
          WHERE origin_airport_id = (
                SELECT id FROM airports
                 WHERE city LIKE 'fiftyville')
            AND year = 2021 AND month = 7 AND day = 29
       ORDER BY hour ASC, minute ASC LIMIT 1);

                                --+---------------+
                                --|     city      |
                                --+---------------+
--The city the thief ESCAPED TO:  | New York City |
                                --+---------------+

-- 6) who helped "Bruce"?
SELECT name FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
AND caller = (
	SELECT phone_number FROM people
	 WHERE name = "Bruce");

                    --+-------+
                    --| name  |
                    --+-------+
                    --| Robin |
                    --+-------+
