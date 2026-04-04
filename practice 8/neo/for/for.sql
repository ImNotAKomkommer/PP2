[ <<label>> ]
for loop_counter in [ reverse ] from.. to [ by step ] loop
    statements
end loop [ label ];
--  
do
$$
begin
   for counter in 1..5 loop
	raise notice 'counter: %', counter;
   end loop;
end;
$$;
--
do $$
begin
   for counter in reverse 5..1 loop
      raise notice 'counter: %', counter;
   end loop;
end; $$
--
do $$
begin
  for counter in 1..6 by 2 loop
    raise notice 'counter: %', counter;
  end loop;
end; $$
--
[ <<label>> ]
for target in query loop
    statements
end loop [ label ];

