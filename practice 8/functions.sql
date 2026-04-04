CREATE OR REPLACE FUNCTION search_phonebook(pattern_text TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone
    FROM phonebook p
    WHERE p.first_name ILIKE '%' || pattern_text || '%'
       OR p.last_name ILIKE '%' || pattern_text || '%'
       OR p.phone ILIKE '%' || pattern_text || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phonebook_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;