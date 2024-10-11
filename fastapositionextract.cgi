#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

# Create a new CGI object
my $cgi = CGI->new;

# Check if the user has uploaded a file
if ($cgi->request_method eq 'POST') {
    my $uploaded_file = $cgi->upload('fasta_file');
    my $start_pos = $cgi->param('start_position');
    my $end_pos = $cgi->param('end_position');
    
    # Handle missing file or parameters
    unless ($uploaded_file && defined $start_pos && defined $end_pos) {
        print $cgi->header(-type => 'text/html');
        print $cgi->start_html(-title => 'FASTA Sequence Extractor');
        print "<div style='text-align: center; padding-top: 50px;'>";
        print $cgi->h2("Error: Missing file or positions.");
        print "</div>";
        print $cgi->end_html;
        exit;
    }

    # Validate and parse positions
    if ($start_pos !~ /^\d+$/ || $end_pos !~ /^\d+$/ || $start_pos > $end_pos) {
        print $cgi->header(-type => 'text/html');
        print $cgi->start_html(-title => 'FASTA Sequence Extractor');
        print "<div style='text-align: center; padding-top: 50px;'>";
        print $cgi->h2("Error: Invalid start or end positions.");
        print "</div>";
        print $cgi->end_html;
        exit;
    }

    # Get the original file name and extract the first two letters
    my $original_filename = $cgi->param('fasta_file');
    my $short_name = substr($original_filename, 0, 2);

    # Read the uploaded file
    my @lines = <$uploaded_file>;
    close($uploaded_file);

    # Process the FASTA sequences
    my $output = '';
    my $sequence = '';
    my $header;
    foreach my $line (@lines) {
        chomp $line;
        if ($line =~ /^>/) {
            # Save the previous sequence if it exists
            if ($header && $sequence) {
                my $extracted = substr($sequence, $start_pos - 1, $end_pos - $start_pos + 1);
                $output .= ">$header\n$extracted\n";
            }
            # Start a new sequence
            $header = substr($line, 1);  # Remove '>'
            $sequence = '';
        } else {
            $sequence .= $line;
        }
    }

    # Handle the last sequence
    if ($header && $sequence) {
        my $extracted = substr($sequence, $start_pos - 1, $end_pos - $start_pos + 1);
        $output .= ">$header\n$extracted\n";
    }

    # Define the file name for download using the first two letters and positions
    my $filename = "${short_name}_extracted_${start_pos}_${end_pos}.txt";

    # Serve the output file for download
    print $cgi->header(
        -type => 'text/plain',
        -attachment => $filename
    );
    print $output;

    exit;
}

# Display the HTML form if no POST request
print $cgi->header(-type => 'text/html');
print $cgi->start_html(
    -title => 'FASTA Sequence Extractor',
    -head => [ $cgi->meta({-charset => 'UTF-8'}) ]
);

# Start centered content
print "<div style='text-align: center; padding-top: 50px;'>";

# Add a space for the logo
print "<img src='http://localhost/posex.png' alt='Logo' style='max-width: 500px; margin-bottom: 20px;'>";  # Replace with actual logo path

# Display the form title
print "<h1>FASTA Sequence Extractor</h1>";
print "<p>Please upload a FASTA file and specify the start and end positions to extract sequences.</p>";

# Create the form
print $cgi->start_form(
    -method => 'POST',
    -enctype => 'multipart/form-data'
);

# File input
print $cgi->filefield(-name => 'fasta_file', -size => 50), "<br><br>";

# Start and end position input
print $cgi->textfield(-name => 'start_position', -size => 10, -placeholder => 'Enter Start Position'), "<br><br>";
print $cgi->textfield(-name => 'end_position', -size => 10, -placeholder => 'Enter End Position'), "<br><br>";

# Submit button
print $cgi->submit(-value => 'Submit');

# End the form and the centered div
print $cgi->end_form;
print "</div>";

# End the HTML
print $cgi->end_html;

