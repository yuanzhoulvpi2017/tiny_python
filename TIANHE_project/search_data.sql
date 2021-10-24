select t.* from huzheng.public.css_location t
where t.time_format = to_char(now() +'8 hours', 'yyyy-mm-dd hh24:MI:ss')
limit 10;


select now();
select current_timestamp + '8 hours';

select to_char(now() +'8 hours', 'yyyy-mm-dd hh24:MI:ss');