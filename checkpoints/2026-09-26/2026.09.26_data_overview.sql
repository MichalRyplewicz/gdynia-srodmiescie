--1.Total hours booked per facility in September 2012
SELECT  (SELECT name FROM cd.facilities fac WHERE bok.facid = fac.facid) AS facility_name, 
SUM(bok.slots)/2.0 AS "total hours"
FROM cd.bookings bok

WHERE bok.starttime >= '2012-09-01' AND bok.starttime < '2012-10-01'
GROUP BY bok.facid

ORDER BY "total hours" DESC
;

-- 2. Members with at least 20 bookings (guest, memid = 0, excluded)
SELECT (SELECT mem.firstname || ' ' ||mem.surname  FROM cd.members mem WHERE bok.memid = mem.memid)AS member, COUNT(bok.memid) AS no_of_res
FROM cd.bookings bok 
WHERE bok.memid != 0
GROUP BY bok.memid
HAVING COUNT(bok.memid) >= 20
ORDER BY no_of_res DESC
;

--3. Revenue of each of facilities divided between members and guests
SELECT (SELECT name FROM cd.facilities fac WHERE bok.facid = fac.facid) AS facility_name, 
    SUM(CASE WHEN bok.memid != 0 THEN bok.slots * fac.membercost
     ELSE 0 END )AS member_revenue,
    SUM(CASE WHEN bok.memid = 0 THEN bok.slots*fac.guestcost
    ELSE 0 END ) AS guest_revenue
FROM cd.bookings bok
JOIN cd.facilities fac
ON bok.facid = fac.facid
GROUP BY bok.facid