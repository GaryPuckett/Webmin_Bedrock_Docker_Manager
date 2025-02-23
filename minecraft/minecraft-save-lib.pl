=head1 Minecraft Save Library

This library provides functions to load and save the configuration for your
Minecraft Bedrock Docker server module, merging in default values for any settings
that aren’t already set.
=cut

BEGIN { push(@INC, ".."); }
use WebminCore;
init_config();

use strict;
use warnings;
use JSON;
use File::Basename;

# Use the fully qualified variable from the main package.
# If it’s not set, default to the current directory.
my $module_config_directory = $main::module_config_directory || '.';

# Define default configuration settings
my %default_config = (
    container_name      => 'mc_bedrock',
    port                => '19132',
    volume              => '/path/to/data',
    restart_policy      => 'unless-stopped',
    name                => 'Bedrock Server',
    world               => 'Bedrock level',
    gamemode            => 'survival',
    difficulty          => 'easy',
    max_players         => '10',
    white_list          => '0',
    allow_cheats        => '0',
    player_idle_timeout => '30',
);

# Configuration file path (using the module configuration directory)
my $config_file = "$module_config_directory/mc_config.json";

# Load configuration from the file and merge with defaults
sub load_config {
    my $config = {};
    if (-e $config_file) {
        open my $fh, '<', $config_file or die "Could not open $config_file: $!";
        local $/;
        my $json_text = <$fh>;
        close $fh;
        $config = decode_json($json_text);
    }
    # Merge in defaults for any missing values
    foreach my $key (keys %default_config) {
        if (!exists $config->{$key} || !defined $config->{$key} || $config->{$key} eq '') {
            $config->{$key} = $default_config{$key};
        }
    }
    return $config;
}

# Save the current configuration to the file
sub save_config {
    my ($config) = @_;
    open my $fh, '>', $config_file or die "Could not open $config_file: $!";
    print $fh encode_json($config);
    close $fh;
}

1;
