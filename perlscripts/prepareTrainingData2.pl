use warnings;
use strict;
use DBI; 


my $ticker='^FTSE';
open (MYFILE, '>trainingdata.txt');
# print MYFILE "Bob\n";
 #close (MYFILE); 
 
my $db=DBI->connect("dbi:mysql:stock", 'root', 'fil1202job') || die( $DBI::errstr . "\n" );

my $SEL = "SELECT a.5dMA, a.10dMA, a.30dMA, a.50dMA, a.100dMA, a.200dMA, a.close,'OUTPUT',if((a.NextDayClose > a.close),1,-1) as result  
from 
(SELECT id, ticker, qdate, close, 5dMA, 10dMA, 30dMA, 50dMA, 100dMA, 200dMA, NextDayClose
FROM stock.stocksscaled
where ticker='$ticker'
and NextDayClose is not null
order by qdate desc
limit 1200) a
LEFT JOIN
(SELECT id, ticker, qdate, close, 5dMA, 10dMA, 30dMA, 50dMA, 100dMA, 200dMA, NextDayClose
FROM stock.stocksscaled
where ticker='&ticker'
and NextDayClose is not null
order by qdate desc
limit 200) b USING (id)
WHERE b.id IS NULL
order by a.qdate desc";

my $sth = $db->prepare($SEL);
 $sth->execute();
 my $count=0;
my $results = $db->selectall_arrayref($SEL);
for my $row (@$results) {
   #my ($ticker) = @$row;
   if ($count > 199)
   {
 print MYFILE "@$row\n";
    } 
    $count = $count+1;

   }	