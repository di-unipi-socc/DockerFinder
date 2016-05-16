    use Sys::Info;


 use Linux::Distribution qw(distribution_name distribution_version);
   use Linux::Distribution qw(distribution_name distribution_version);

    my $info = Sys::Info->new;
    printf "Perl version is %s\n", $info->perl;
    if(my $httpd = $info->httpd) {
        print "HTTP Server is $httpd\n";
    }
    my $cpu = $info->device('CPU');
    my $os  = $info->os;
    printf "Operating System is %s\n", $os->name( long => 1 );
    printf "CPU: %s\n", scalar $cpu->identify;



  if(my $distro = distribution_name) {
        my $version = distribution_version();
        print "you are running $distro, version $version\n";
  } else {
        print "distribution unknown\n";
  }

