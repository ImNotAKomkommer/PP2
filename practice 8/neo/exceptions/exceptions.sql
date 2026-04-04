do $$

declare
    counter int := 0;
begin

  loop
  	counter = counter + 1;
	raise notice '%', counter;
	exit when counter = 5;
  end loop;

end;

$$;
--
do
$$
declare
	rec record;
	v_film_id int = 2000;
begin
	-- select a film
	select film_id, title
	into strict rec
	from film
	where film_id = v_film_id;
end;
$$
language plpgsql;
--
do
$$
declare
	rec record;
	v_film_id int = 2000;
begin
	-- select a film
	select film_id, title
	into strict rec
	from film
	where film_id = v_film_id;
        -- catch exception
	exception
	   when no_data_found then
	      raise exception 'film % not found', v_film_id;
end;
$$;
--
do
$$
declare
	rec record;
begin
	-- select film
	select film_id, title
	into strict rec
	from film
	where title LIKE 'A%';

	exception
	   when too_many_rows then
	      raise exception 'Search query returns too many rows';
end;
$$;
--
do
$$
declare
	rec record;
	v_length int = 90;
begin
	-- select a film
	select film_id, title
	into strict rec
	from film
	where length = v_length;

        -- catch exception
	exception
	   when sqlstate 'P0002' then
	      raise exception 'film with length % not found', v_length;
	   when


