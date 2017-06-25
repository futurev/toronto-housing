

CREATE TABLE records (
  id varchar(50) PRIMARY KEY,
  type char(10),
  scraped boolean
)
;


CREATE TABLE sale_records (
  id varchar(50) PRIMARY KEY,
  address1 varchar(200),
  address2 varchar(200),
  bedrooms varchar(5),
  community varchar(100),
  postal varchar(10),
  rooms varchar(10),
  sold integer,
  list integer,
  sold_date date,
  list_date date,
  property_type varchar(50),
  location geography(POINT,4326)
)
;


CREATE TABLE list_records (
  id varchar(50) PRIMARY KEY,
  address1 varchar(200),
  address2 varchar(200),
  bedrooms varchar(5),
  community varchar(100),
  postal varchar(10),
  rooms varchar(10),
  list integer,
  list_date date,
  property_type varchar(50),
  location geography(POINT,4326)
)
;


CREATE INDEX records_id ON records (id);
CREATE INDEX records_type ON records (type);
CREATE INDEX list_records_id ON list_records (id);
CREATE INDEX sale_records_id ON sale_records (id);


ANALYZE records (id, type, scraped);
ANALYZE list_records (id);
ANALYZE sale_records (id);


CREATE TABLE sale_records (
  id varchar(20) PRIMARY KEY,
  city varchar(50),
  area varchar(50),
  solddate date,
  inputdate date,
  soldprice integer,
  askprice integer,
  stname varchar(50),
  stno varchar(10),
  sttype varchar(20),
  status varchar(20),
  style varchar(50),
  type varchar(50),
  wshrm integer,
  bdrm integer,

  location geography(POINT,4326)
)
;


CREATE TABLE list_records (
  id varchar(20) PRIMARY KEY,
  city varchar(50),
  area varchar(50),
  inputdate date,
  askprice integer,
  stname varchar(50),
  stno varchar(10),
  sttype varchar(20),
  status varchar(20),
  style varchar(50),
  type varchar(50),
  wshrm integer,
  bdrm integer,

  location geography(POINT,4326)
)
;


CREATE INDEX list_records_id ON list_records (id);
CREATE INDEX sale_records_id ON sale_records (id);

ANALYZE list_records (id);
ANALYZE sale_records (id);
