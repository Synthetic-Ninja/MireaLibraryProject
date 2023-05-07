CREATE OR REPLACE FUNCTION check_count() RETURNS TRIGGER AS $check_count$
    BEGIN
        IF (TG_OP = 'UPDATE') THEN
            IF NEW.count = 0 AND NEW.is_empty = false THEN
                NEW.is_available = false;
                NEW.is_empty = true;
                return NEW;
            END IF;
            IF NEW.count > 0 AND NEW.is_empty = true THEN
                NEW.is_available = true;
                NEW.is_empty = false;
                return NEW;
            END IF;
        END IF;

    RETURN NEW;
    END

$check_count$ language plpgsql;
CREATE OR REPLACE TRIGGER check_rates BEFORE UPDATE ON "Books_book"
FOR EACH ROW EXECUTE PROCEDURE check_count();
