#!/usr/bin/perl
use WebminCore;
init_config();

# Update the EULA setting
$config{'EULA'} = '1';

# Save the updated configuration
save_module_config(\%config);

# Redirect back to the main page
print "Location: ../index.cgi\n\n";