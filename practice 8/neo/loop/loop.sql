[ <<label>> ]
for target in query loop
    statements
end loop [ label ];
--
<<label>>
loop
   statements;
   if condition then
      exit;
   end if;
end loop;
--
<<outer>>
loop
   statements;
   <<inner>>
   loop
     /* ... */
     exit <<inner>>
   end loop;
end loop;
--
do $$

declare
    counter int := 0;
begin

  loop
  	counter = counter + 1;
	raise notice '%', counter;

	if counter = 5 then
		exit;
	end if;

  end loop;

end;

$$;
--
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
