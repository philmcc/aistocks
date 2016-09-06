
use warnings;
use strict;
use DBI; 



my $db1=DBI->connect("dbi:mysql:stock", 'root', 'fil1202job') || die( $DBI::errstr . "\n" );
my $SEL = "call populate_NDC";
my $sth = $db1->prepare($SEL);
$sth->execute();
