CREATE TABLE passport (
	id VARCHAR PRIMARY KEY, -- номер паспорта
	issue DATE NOT NULL, -- дата выдачи
	authority TEXT NOT NULL, -- кем выдан
	address TEXT NOT NULL -- адрес регистрации
);

CREATE TABLE contract (
	id SERIAL PRIMARY KEY, -- номер контракта
	signed DATE NOT NULL, -- дата заключения
	"type" VARCHAR NOT NULL -- тип контракта (временный/постоянный) 
);

CREATE TABLE employee (
	personnel_number SERIAL PRIMARY KEY, -- табельный номер
	contract INTEGER NOT NULL UNIQUE REFERENCES contract(id) ON UPDATE CASCADE ON DELETE CASCADE, -- номер контракта
	fullname VARCHAR NOT NULL,
	gender CHAR NOT NULL, -- 'f'/'m'
	birth DATE NOT NULL, -- день рождения
	education VARCHAR NOT NULL, -- образование (срденее неполное, среднее полное, среднее специальное, неоконченное высшее, высшее)
	degree VARCHAR CHECK (education IN ('высшее') OR degree IS NULL), -- академическая степень (бакалавр, специалист, магистр, к.н., д.н.)
	programme VARCHAR CHECK (education IN ('высшее', 'высшее неоконченное') OR programme IS NULL), -- профиль подготовки, напр. компьютерная безопасность, информационные системы, пр.
	family_status SMALLINT NOT NULL, -- {0:холост/незамужем, 1:женат/замужем, 2:разведён/разведена, 3:вдовец/вдова}
	address TEXT, -- адрес проживания
	phone BIGINT CHECK (phone > 0), -- телефон
	experience DATE, -- начало стажа работы
	passport VARCHAR NOT NULL REFERENCES passport(id) ON UPDATE CASCADE ON DELETE CASCADE -- данные паспорта
);


CREATE TABLE personnel_schedule (
	code SERIAL PRIMARY KEY, -- код должности
	position VARCHAR NOT NULL, -- должность (инженер, доцент, зав. кафедрой и пр.)
	rank VARCHAR, -- разярд, напр.: 1-й, 2-й, 3-й или младший, старший
	category VARCHAR NOT NULL, -- категория, напр. (профессорско-преподавательский состав, технический персонал, административный состав, хозяйственный состав и т.д.
	salary NUMERIC(13, 4) NOT NULL DEFAULT 0.0000, -- ну кто может получить запрлату больше 9 миллионов?
	rate_amount REAL NOT NULL, -- число доступных ставок
	rate_booked REAL NOT NULL DEFAULT 0.00 CHECK (rate_booked <= rate_amount), -- число занятынх ставок
	employees SMALLINT NOT NULL DEFAULT 0, -- число занятых сотрудников
	UNIQUE (position, rank, category)
);

CREATE TABLE employee_has_position (
	employee INTEGER NOT NULL REFERENCES employee(personnel_number) ON UPDATE CASCADE ON DELETE CASCADE,
	position INTEGER NOT NULL REFERENCES personnel_schedule(code) ON UPDATE CASCADE ON DELETE CASCADE,
	rate REAL NOT NULL CHECK (rank IN (0.25, 0.5, 1.0)), -- ставка
	PRIMARY KEY (employee, position)
);