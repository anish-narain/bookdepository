PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('45320fb27815');
CREATE TABLE books (
	book_id INTEGER NOT NULL, 
	isbn VARCHAR(30), 
	title VARCHAR(120), 
	author VARCHAR(120), 
	grade VARCHAR(30), 
	examboard VARCHAR(30), 
	publisher VARCHAR(120), 
	subject VARCHAR(30), 
	PRIMARY KEY (book_id)
);
CREATE TABLE branch (
	branch_id INTEGER NOT NULL, 
	branch_name VARCHAR(120), 
	city VARCHAR(60), 
	address VARCHAR(200), 
	phone_number VARCHAR(20), 
	email VARCHAR(60), 
	contact_person VARCHAR(60), 
	PRIMARY KEY (branch_id)
);
CREATE TABLE notification_template (
	template_id INTEGER NOT NULL, 
	template_name VARCHAR(60), 
	template_text VARCHAR(3000), 
	PRIMARY KEY (template_id)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(64), 
	email VARCHAR(120), 
	password_hash VARCHAR(128), 
	is_user BOOLEAN, 
	PRIMARY KEY (id), 
	CHECK (is_user IN (0, 1))
);
CREATE TABLE bookitem (
	book_item_id INTEGER NOT NULL, 
	book_id INTEGER, 
	status VARCHAR(30), 
	acquisition_date DATE, 
	promise_date DATE, 
	branch_id INTEGER, 
	PRIMARY KEY (book_item_id), 
	FOREIGN KEY(book_id) REFERENCES books (book_id), 
	FOREIGN KEY(branch_id) REFERENCES branch (branch_id)
);
CREATE TABLE transactions (
	transaction_id INTEGER NOT NULL, 
	book_item_id INTEGER, 
	transaction_account INTEGER, 
	transaction_type VARCHAR(30), 
	transaction_date DATETIME, 
	award_points INTEGER, 
	PRIMARY KEY (transaction_id), 
	FOREIGN KEY(book_item_id) REFERENCES bookitem (book_item_id), 
	FOREIGN KEY(transaction_account) REFERENCES user (id)
);
CREATE INDEX ix_books_author ON books (author);
CREATE UNIQUE INDEX ix_books_isbn ON books (isbn);
CREATE INDEX ix_books_title ON books (title);
CREATE UNIQUE INDEX ix_user_email ON user (email);
CREATE UNIQUE INDEX ix_user_username ON user (username);
COMMIT;
