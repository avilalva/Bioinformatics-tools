#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

# Print the HTML header
print header();
print start_html(
    -title  => 'FASTA Sequence Counter',
    -style  => {-src => 'https://example.com/style.css'}  # You can change to your CSS if needed
);

# HTML form to upload multiple files
print "<div style='text-align: center; padding-top: 50px;'>";
print "<img src='http://localhost/seqcounter.png' alt='Logo' style='max-width: 500px; margin-bottom: 20px;'>"; # Change the image URL
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

            my $fasta_data = '';
            
            # Read the file content
            while (<$file_handle>) {
                $fasta_data .= $_;
            }
            
            # Count the number of FASTA sequences
            my $fasta_count = () = $fasta_data =~ /^>/mg;
            
            # Display the count for each file
            print "<h2>Number of sequences in $file_name is: $fasta_count</h2>";
        }
        
        print "</div>";
    } else {
        print "<div style='text-align: center;'><p>Error: Could not read the files.</p></div>";
    }
}

print end_html();

