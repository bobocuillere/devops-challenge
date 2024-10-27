CREATE TABLE sinch_test_table (
    id SERIAL PRIMARY KEY,
    data TEXT
);

-- Insert data
INSERT INTO sinch_test_table (data) VALUES ('Sample data');

-- Select data
SELECT * FROM sinch_test_table;

-- Update data
UPDATE sinch_test_table SET data = 'Updated data' WHERE id = 1;

-- Delete data
DELETE FROM sinch_test_table WHERE id = 1;
