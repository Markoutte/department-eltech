create function get_employee(INTEGER)
returns table(
	personnel_number INTEGER, -- табельный номер
	contract_id INTEGER, -- номер контракта
	signed VARCHAR, -- дата заключения
	"type" VARCHAR, -- тип контракта (временный/постоянный) 
	fullname VARCHAR,
	gender CHAR, -- 'f'/'m'
	birth VARCHAR, -- день рождения
	education VARCHAR, -- образование (срденее неполное, среднее полное, среднее специальное, неоконченное высшее, высшее)
	degree VARCHAR , -- академическая степень (бакалавр, специалист, магистр, к.н., д.н.)
	programme VARCHAR, -- профиль подготовки, напр. компьютерная безопасность, информационные системы, пр.
	family_status SMALLINT, -- {0:холост/незамужем, 1:женат/замужем, 2:разведён/разведена, 3:вдовец/вдова}
	current_address TEXT, -- адрес проживания
	phone BIGINT, -- телефон
	experience VARCHAR, -- начало стажа работы
	passport_id VARCHAR, -- номер паспорта
	issue VARCHAR, -- дата выдачи
	authority TEXT, -- кем выдан
	passport_address TEXT -- адрес регистрации
) as $$
	select personnel_number, c.id contract_id, to_char(signed, 'DD.MM.YYYY'), "type", fullname, gender, to_char(birth, 'DD.MM.YYYY'), 
		education, degree, programme, family_status, e.address current_address, phone, to_char(experience, 'DD.MM.YYYY'), 
		p.id passport_id, to_char(issue, 'DD.MM.YYYY'), authority, p.address passport_address
	from employee e, passport p, contract c
	where personnel_number = $1
	  and e.passport = p.id
	  and e.contract = c.id;
$$ language 'sql';

select * from get_employee(3);

drop function get_employee(text);