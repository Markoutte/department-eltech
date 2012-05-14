CREATE OR REPLACE FUNCTION update_schedule()
RETURNS TRIGGER AS
$$ 
DECLARE
	var_parts real;
	var_employees int;

BEGIN
IF TG_OP = 'INSERT' THEN
	var_parts = (SELECT rate_booked FROM personnel_schedule WHERE code = NEW.position);
	var_employees = (SELECT employees FROM personnel_schedule WHERE code = NEW.position);
	UPDATE personnel_schedule
	SET rate_booked = var_parts + NEW.rate, employees = var_employees + 1
	WHERE code = NEW.position;
	RETURN NEW;
ELSEIF TG_OP = 'UPDATE' THEN
	var_parts = (SELECT rate_booked FROM personnel_schedule WHERE code = NEW.position);
	UPDATE personnel_schedule
	SET rate_booked = var_parts - OLD.rate + NEW.rate
	WHERE code = NEW.position;
	RETURN NEW;
ELSEIF TG_OP = 'DELETE' THEN
	var_parts = (SELECT rate_booked FROM personnel_schedule WHERE code = OLD.position);
	var_employees = (SELECT employees FROM personnel_schedule WHERE code = OLD.position);
	UPDATE personnel_schedule
	SET rate_booked = var_parts - OLD.rate, employees = var_employees - 1
	WHERE code = OLD.position;
	RETURN OLD;
END IF;
END; $$
LANGUAGE plpgsql;

CREATE TRIGGER update_schedule
AFTER INSERT OR UPDATE OR DELETE 
ON employee_has_position
FOR EACH ROW EXECUTE PROCEDURE update_schedule();

