use warnings;
use strict;
use DBI; 



open (MYFILE, '>testdata.txt');
 
my $db=DBI->connect("dbi:mysql:stock", 'root', 'fil1202job') || die( $DBI::errstr . "\n" );

my $ticker='^FTSE';

my $SEL = "SELECT a.5dMA, a.10dMA, a.30dMA, a.50dMA, a.100dMA, a.200dMA, a.close,'OUTPUT',if((a.NextDayClose > a.close),1,-1) as result   
FROM stock.stocksscaled a
where ticker='^FTSE'
and NextDayClose is not null
order by qdate desc
limit 200";

my $sth = $db->prepare($SEL);
 $sth->execute();
 
my $results = $db->selectall_arrayref($SEL);
for my $row (@$results) {
  
 print MYFILE "@$row\n";
     

   }	
  close (MYFILE);