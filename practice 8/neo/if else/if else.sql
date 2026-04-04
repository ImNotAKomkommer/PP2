if condition then
   statements;
end if;
--
do $$
declare
  selected_film film%rowtype;
  input_film_id film.film_id%type = 0;
begin

  select * from film
  into selected_film
  where film_id = input_film_id;

  if not found then
     raise notice'The film % could not be found',
	    input_film_id;
  end if;
end $$;
--
if not found then
   raise notice'The film % could not be found', input_film_id;
end if; 
--
if condition then
  statements;
else
  alternative-statements;
end if;
--
do $$
declare
  selected_film film%rowtype;
  input_film_id film.film_id%type := 100;
begin

  select * from film
  into selected_film
  where film_id = input_film_id;

  if not found then
     raise notice 'The film % could not be found',
	    input_film_id;
  else
     raise notice 'The film title is %', selected_film.title;
--
if condition_1 then
  statement_1;
elsif condition_2 then
  statement_2
...
elsif condition_n then
  statement_n;
else
  else-statement;
end if;

