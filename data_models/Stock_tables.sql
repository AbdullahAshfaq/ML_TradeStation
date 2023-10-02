create table if not exists BTCUSDT (
uuid varchar(128),
ts float not null,
currentts float not null,
volume float not null,
price float not null,
PRIMARY KEY (`ts`)
);

create table if not exists AAPL (
uuid varchar(128),
ts float not null,
currentts float not null,
volume float not null,
price float not null,
PRIMARY KEY (`ts`)
);

create table if not exists AAPL_news (
	datetime float not null,
	source varchar(64) not null,
	headline varchar(256) not null,
	summary varchar(5120) not null,
	PRIMARY KEY (`datetime`,`source`,`headline`)
);


# Explanation of mspr: https://medium.com/@stock-api/finnhub-insiders-sentiment-analysis-cc43f9f64b3a
# mspr: Monthly share purchase ratio

create table if not exists insider_sentiment (
symbol varchar(20) not null,
year int not null,
month int not null,
`change` float not null,
mspr float not null,
PRIMARY KEY (`symbol`,`year`,`month`)
);



