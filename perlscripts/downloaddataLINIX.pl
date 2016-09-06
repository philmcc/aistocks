use warnings;
use strict;
use DBI; 
use Date::Simple;
use LWP::Simple;
use Text::CSV_XS;


update_db();

#############################
##SUBS
#############################
sub update_db {

my $db=DBI->connect("dbi:mysql:stock", 'root', 'fil1202job') || die( $DBI::errstr . "\n" );

my $SEL = "SELECT ticker FROM stock.tickers";
my $sth = $db->prepare($SEL);
 $sth->execute();
 
my $results = $db->selectall_arrayref($SEL);
for my $row (@$results) {
   my ($ticker) = @$row;
 print "$ticker\n";
     
my $filenamevar;
$filenamevar=download_data($ticker,"2004-6-2");
if ($filenamevar ne "none"){
insert_csv($filenamevar, $ticker);
    } 
   }	
}

###################################################
###################################################
sub download_data {
my $vticker;
my $startdate;
my $maxdate;
my $filename;

#$vticker="^FTSE";
#$startdate="2004-06-01";
$vticker=$_[0];
$startdate=$_[1];

print "sub download_data - $vticker\n";
## Open DB Connection and find last Date with Data
my $db=DBI->connect("dbi:mysql:stock", 'root', 'fil1202job') || die( $DBI::errstr . "\n" );
my $SEL = "SELECT ifnull(max(qdate),\"$startdate\") FROM stock.stocks where ticker = \"$vticker\"";
my $ref = $db->selectall_arrayref($SEL);
$maxdate = $$ref[0][0];
##################################################

## Populate the date fields
## Last data date
my ($max_YYYY, $max_MM, $max_DD)= split(/-/,$maxdate);
print "Last Date is $max_YYYY-$max_MM-$max_DD\n";
##todays date
my($today_day, $today_month, $today_year)=(localtime)[3,4,5];
$today_month=$today_month+1;
$today_year=$today_year+1900;
##################################################

## Create URL
my $today_month1 = $today_month - 1;
my $max_MM1 = $max_MM - 1;

my $url = "http://ichart.finance.yahoo.com/table.csv?s=%5EFTSE&d=$today_month1&e=$today_day&f=$today_year&g=d&a=$max_MM1&b=$max_DD&c=$max_YYYY&ignore=.csv";
print "$url\n";
##################################################

## Download file
$filename="quote_"."$vticker"."_"."$today_year"."$today_month"."$today_day".".csv";
print "$filename\n";
my $file = $filename;
print "$url\n";

#my $downloadfile=getstore($url, $file);
#print "$downloadfile\n";
#my $var=`wget -O $file $url`;
#my $var1-`(cat header.txt; wget -O - --quiet $url | sed 1d) > $filename`;
my $var2=`curl --output $filename '$url' `;
###################################################
if (-e $filename) {
# print "File Exists!";
print "$file Downloaded!\n";
$SEL = "update stock.tickers set lastupdate = sysdate() where ticker='$vticker'";
my $sth = $db->prepare($SEL);
$sth->execute();
return $filename;
}
unless (-e $filename) {
# print "File Doesn't Exist!";
print "No Data!\n";
 return "none";
 } 

}

###################################################
###################################################
sub insert_csv {

my $db1=DBI->connect("dbi:mysql:stock", 'root', 'fil1202job') || die( $DBI::errstr . "\n" );
my $SEL = "INSERT INTO `stock`.`stocks`(`ticker`,`qdate`,`open`,`low`,`high`,`close`,`volume`) VALUES(?,?,?,?,?,?,?)";
my $sth = $db1->prepare($SEL);
my $file = $_[0]; 
open(my $data, '<', $file) or die "Could not open '$file' $!\n";
print "Begining insert of $file\n";
my $num = 0;
while (my $line = <$data>) 
#while (my $line = <$data> and  $num < 200)
{
    chomp $line;
    if ($num != 0  )
        {
        my @fields = split "," , $line;
        my $d = $fields[0]; 
        #print "@fields";
        $sth->execute($_[1],$d,$fields[1],$fields[2],$fields[3],$fields[4],$fields[5]);
        }
    $num=$num + 1;
}

print "$_[0] Inserted\n";


}

