-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE month = 07 AND day = 28 AND street = 'Humphrey Street';
SELECT transcript, name FROM interviews WHERE transcript LIKE '%bakery%';
SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 07 AND activity = 'exit' AND hour = 10 AND minute >=15 AND minute < 25;
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 07 AND activity = 'exit' AND hour = 10 AND minute >=15 AND minute < 25);
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 07 AND atm_location = 'Leggett Street'));
SELECT caller, receiver, duration FROM phone_calls WHERE day = 28 AND month = 07 AND receiver IN (SELECT phone_number FROM people WHERE name = 'Diana');
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE day = 28 AND month = 07 AND caller = '(770) 555-1861');
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 07 AND receiver = '(770) 555-1861');
SELECT flight_id FROM passengers WHERE passport_number IN (SELECT passport_number FROM people WHERE name = 'Diana') AND flight_id IN (SELECT id FROM flights WHERE day = 29 AND month = 07);
SELECT destination_airport_id, origin_airport_id, hour, minute FROM flights WHERE id = 18;
SELECT city FROM airports WHERE id = 8 OR id = 4;
SELECT seat FROM passengers WHERE flight_id = 51 AND passport_number = (SELECT passport_number FROM people WHERE name = 'Margaret');.
