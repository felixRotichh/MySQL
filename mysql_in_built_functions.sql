show databases;
create database employees;
use employees;

drop database employees;

use sql_intro;
show tables;

describe employees;

select distinct city from employees;
select distinct city from employees;

select avg(age) from employees;

#avg age in each dept
select dept, round(avg(age),1) as avg_age from employees 
group by dept;

select dept, sum(salary) as total_salary from employees 
group by dept;
select dept, avg(salary) as avg_salary from employees 
group by dept;

select count(emp_id), city from employees
group by city
order by count(emp_id) desc;

select year(doj) as year, count(emp_id) from employees
group by year(doj);


create table sales (product_id int, sell_price float, quantity int,
state varchar(20));
insert into sales values
(120, 250, 15, "Nakuru"),
(121, 270, 12, "Nairobi"),
(122, 298, 7, "Kisumu"),
(121, 255, 9, "Eldoret"),
(122, 655, 9, "Mombasa"),
(120, 457, 23, "Rongai"),
(123, 160, 43, "Embu"),
(123, 270, 32, "Kiambu"),
(120, 350, 5, "Bomet"),
(121, 550, 9, "Thika"),
(132, 260, 23, "Kericho");

select * from sales;
select product_id, sum(sell_price * quantity) as revenue
from sales group by product_id;

create table c_product(product_id int, cost_price float);

insert into c_product values
(120, 170),
(121, 100),
(122, 130),
(123, 188),
(132, 90);

# calculate profit
select c.product_id, sum((s.sell_price - c.cost_price) * s.quantity)
as profit from sales as s inner join c_product as c
where s.product_id = c.product_id
group by c.product_id;

# Having clause in sql
select dept, avg(salary) as avg_salary
from employees
group by dept
having avg(salary) > 50000;

select city, sum(salary) as total from employees
group by city
having sum(salary) > 80000;

select dept, count(*) as emp_count
from employees
group by dept
having count(*)>1;