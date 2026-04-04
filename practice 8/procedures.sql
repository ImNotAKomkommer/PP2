CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE first_name = p_first_name
          AND last_name = p_last_name
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_first_name
          AND last_name = p_last_name;
    ELSE
        INSERT INTO phonebook (first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_many_users(
    IN p_first_names TEXT[],
    IN p_last_names TEXT[],
    IN p_phones TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS temp_incorrect_data (
        first_name TEXT,
        last_name TEXT,
        phone TEXT
    ) ON COMMIT DROP;

    TRUNCATE temp_incorrect_data;

    IF array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_last_names, 1)
       OR array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i IN 1 .. array_length(p_first_names, 1)
    LOOP
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE first_name = p_first_names[i]
                  AND last_name = p_last_names[i]
            ) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE first_name = p_first_names[i]
                  AND last_name = p_last_names[i];
            ELSE
                INSERT INTO phonebook (first_name, last_name, phone)
                VALUES (p_first_names[i], p_last_names[i], p_phones[i]);
            END IF;
        ELSE
            INSERT INTO temp_incorrect_data (first_name, last_name, phone)
            VALUES (p_first_names[i], p_last_names[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$ LANGUAGE plpgsql;