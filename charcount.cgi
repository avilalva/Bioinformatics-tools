#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

# Print the HTML header
print header();
print start_html(
    -title  => 'FASTA Character Counter',
    -style  => {-src => 'https://example.com/style.css'}  # Optional: change this to your CSS file if needed
);

# HTML form to upload multiple files
print "<div style='text-align: center; padding-top: 50px;'>";

# Add the logo (make sure the path to the image is correct)
print "<img src='http://localhost/charcount.png' alt='Logo' style='max-width: 500px; margin-bottom: 20px;'>";  # Adjust the image path

print "<h1>Upload FASTA Files</h1>";
print start_multipart_form(),
    filefield(-name => 'uploaded_files', -multiple => 'true', -accept => 'text/plain'),
    submit(-value => 'Upload'),
    end_form();
print "</div>";

# Handle file uploads
if (param('uploaded_files')) {
    my @file_params = param('uploaded_files');  # Get the names of the uploaded files
    my @file_handles = upload('uploaded_files');  # Get file handles for the uploaded files

    if (@file_handles) {
        print "<div style='text-align: center; padding-top: 30px;'>";

        # Iterate over each uploaded file
        for (my $i = 0; $i < @file_handles; $i++) {
            my $file_handle = $file_handles[$i];
            my $file_name = $file_params[$i];  # Use param to get the actual uploaded file name

            print "<h2>File: $file_name</h2>";

            my $fasta_data = '';
            my $current_header = '';
            my $seq_data = '';

            # Read the file content line by line
            while (my $line = <$file_handle>) {
                chomp($line);

                # Check if the line starts with '>', indicating a header line
                if ($line =~ /^>/) {
                    # If there's sequence data collected, count the characters and print result
                    if ($seq_data) {
                        my $char_count = length($seq_data);
                        print "<p>Number of characters under $current_header: $char_count</p>";
                        $seq_data = '';  # Reset for the next sequence
                    }
                    $current_header = $line;  # Store the header
                } else {
                    # Concatenate the sequence data
                    $seq_data .= $line;
                }
            }

            # Handle the last sequence
            if ($seq_data) {
                my $char_count = length($seq_data);
                print "<p>Number of characters under $current_header: $char_count</p>";
            }
        }

        print "</div>";
    } else {
        print "<div style='text-align: center;'><p>Error: Could not read the files.</p></div>";
    }
}

print end_html();
