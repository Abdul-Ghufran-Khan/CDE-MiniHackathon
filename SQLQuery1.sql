-- PART 4 (Load Data into SQL Server)

CREATE TABLE BanggoodProducts (
    id INT IDENTITY(1,1) PRIMARY KEY,       -- Auto-increment ID
    title NVARCHAR(MAX),                     -- Product title
    price FLOAT,                             -- Product price
    img NVARCHAR(MAX),                       -- Product image URL
    link NVARCHAR(MAX),                      -- Product link URL
    category NVARCHAR(255),                  -- Product category
    rating FLOAT,                            -- Product rating
    review_count INT,                        -- Number of reviews
    availability NVARCHAR(50)                -- Availability status
);

select * from BanggoodProducts;

SELECT COUNT(*) AS TotalRows
FROM BanggoodProducts;

SELECT category, COUNT(*) AS CountPerCategory
FROM BanggoodProducts
GROUP BY category
ORDER BY CountPerCategory DESC;


-- Part 5 (SQL Aggregated Analysis (Minimum 5 Queries))

--Average price per category
SELECT category, 
       AVG(price) AS AvgPrice
FROM BanggoodProducts
GROUP BY category
ORDER BY AvgPrice DESC;


--Average rating per category
SELECT category, 
       AVG(rating) AS AvgRating
FROM BanggoodProducts
GROUP BY category
ORDER BY AvgRating DESC;

--Product count per category
SELECT category, 
       COUNT(*) AS ProductCount
FROM BanggoodProducts
GROUP BY category
ORDER BY ProductCount DESC;

--Top 5 reviewed items per category
WITH RankedProducts AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY review_count DESC) AS rn
    FROM BanggoodProducts
)
SELECT category, title, review_count, price, rating
FROM RankedProducts
WHERE rn <= 5
ORDER BY category, review_count DESC;

--Stock availability percentage per category
SELECT category,
       COUNT(*) AS TotalProducts,
       SUM(CASE WHEN availability = 'In Stock' THEN 1 ELSE 0 END) AS InStockCount,
       CAST(SUM(CASE WHEN availability = 'In Stock' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS InStockPercentage
FROM BanggoodProducts
GROUP BY category
ORDER BY InStockPercentage DESC;