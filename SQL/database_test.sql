USE LPD_Officer_Monitor;

INSERT INTO
	Officers(officer_id)
Values
	(378666988412731404),
    (566311811637575680);

/*INSERT INTO
	TimePeriods(time_period_name, start_time, end_time)
VALUES
	("Time Period 1", "2020-01-07 15-13-05", "2020-01-07 15-16-49"),
    ("Time Period 2", "2020-01-07 15-17-05", "2020-01-07 15-22-45"),
    ("Time Period 3", "2020-01-07 17-33-33", "2020-01-07 21-16-49");*/

INSERT INTO 
	TimeLog(officer_id, start_time, end_time)
VALUES
	(378666988412731404, "2020-01-07 15-13-05", "2020-01-07 15-15-45"),
    (378666988412731404, "2020-01-07 15-16-33", "2020-01-07 15-16-49"),
    (378666988412731404, "2020-01-07 15-17-05", "2020-01-07 15-22-45"),
    (378666988412731404, "2020-01-07 17-33-33", "2020-01-07 18-33-33"),
    (378666988412731404, "2020-01-07 18-45-53", "2020-01-07 19-13-21"),
    (378666988412731404, "2020-01-07 21-16-33", "2020-01-07 21-16-49");

INSERT INTO TimeLog(officer_id, start_time, end_time) VALUES (378666988412731404, "2020-01-10 15-13-05", "2020-01-11 02-15-45");

SELECT * FROM Officers;
SELECT * FROM TimeLog;

SELECT SUM(end_time - start_time) AS 'Time' FROM TimeLog WHERE officer_id = 378666988412731404;

SELECT * FROM TimeLog WHERE officer_id = 378666988412731404 AND (start_time > '2020-01-07 15:17:04' AND start_time < '2020-01-07 21:16:49');

SELECT start_time, end_time
FROM TimeLog
WHERE
	officer_id = 378666988412731404 AND
	(start_time > '2020-01-07 15:17:04' AND start_time < '2020-01-07 21:16:49');
    
SELECT start_time, end_time, end_time - start_time AS 'duration'
FROM TimeLog
WHERE
	officer_id = 378666988412731404 AND
	(start_time > "2020-03-1 14:32:29" AND start_time < "2020-03-02 14:32:29");

DELETE FROM TimeLog WHERE officer_id = '566311811637575680';
DELETE FROM Officers WHERE officer_id = '566311811637575680';

INSERT INTO 
	MessageActivityLog(message_id, channel_id, officer_id, send_time)
VALUES
	(711212837799985182, 645385529868812348, 507951982808399878, NOW()),
    (711212744581447802, 660935988738129937, 507951982808399878, NOW()),
    (711212727862951947, 697185649949933698, 507951982808399878, NOW()),
    (711212687979184148, 708736137463726131, 507951982808399878, NOW());

SELECT * FROM MessageActivityLog WHERE officer_id = 507951982808399878 AND channel_id = 660935988738129937;
SELECT * FROM MessageActivityLog;

UPDATE MessageActivityLog
SET
	message_id = 711763900915253266,
	send_time = "2020-05-18 02:10:52"
WHERE
	entry_number = 10;
    
UPDATE MessageActivityLog SET message_id = 711763900915253266, send_time = "2020-05-18 02:15:53" WHERE entry_number = 10;

SELECT * FROM MessageActivityLog WHERE officer_id = 378666988412731404;

SELECT officer_id, channel_id, message_id, send_time
FROM MessageActivityLog
WHERE officer_id = 378666988412731404
UNION
SELECT officer_id, 0, 0, end_time AS "send_time"
FROM TimeLog
WHERE officer_id = 378666988412731404
	ORDER BY end_time DESC
    LIMIT 1;