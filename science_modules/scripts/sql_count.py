import psycopg2

servers = ['tao01', 'tao02', 'tao03']
sum = 0
for ii, srv in enumerate(servers):
    conn = psycopg2.connect("dbname='millennium_mini_3servers_v4' user='taoadmin' host='%s' port='3306'"%srv)
    cur = conn.cursor()
    for jj in range(ii, 52, 3):
        cur.execute('SELECT COUNT(*) FROM tree_%d WHERE snapnum=63'%jj)
        sum += int(cur.fetchall()[0][0])
    conn.close()
print sum
