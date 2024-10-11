#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;  # For extracting the filename

# Print the HTML header
print header();
print start_html(
    -title  => 'FASTA CG Content Calculator',
    -style  => {-src => 'https://example.com/style.css'}  # Optional: change this to your CSS file if needed
);

# HTML form to upload a FASTA file
print "<div style='text-align: center; padding-top: 50px;'>";

# Add logo space if needed
print "<img src='http://localhost/gccount.png' alt='Logo' style='max-width: 500px; margin-bottom: 20px;'>";  # Adjust the image path

print "<h1>Upload a FASTA File to Calculate CG Content</h1>";
print start_multipart_form(),
    filefield(-name => 'uploaded_file', -accept => 'text/plain'),
    submit(-value => 'Upload'),
    end_form();
print "</div>";

# Handle the uploaded file
if (param('uploaded_file')) {
    my $uploaded_filename = param('uploaded_file');  # Get the uploaded file name
    my $file_handle = upload('uploaded_file');       # Get the file handle

    if ($file_handle) {
        my $basename = basename($uploaded_filename);  # Extract just the file name (without full path)

        # Print CG content result with file name
        print "<div style='text-align: center; padding-top: 30px;'>";
        print "<h2>CG Content Results for '$basename'</h2>";  # Display file name in heading
        print "<table border='1' cellpadding='5' style='margin: 0 auto;'>";
        print "<tr><th>FASTA Header</th><th>CG Count</th><th>Total Length</th><th>CG Percentage</th></tr>";

        my $current_header = '';
        my $seq_data = '';

        # Read the file content line by line
        while (my $line = <$file_handle>) {
            chomp($line);
            
            # Check if the line is a FASTA header (starts with '>')
            if ($line =~ /^>/) {
                # If we have accumulated sequence data, calculate and print the CG content
                if ($seq_data) {
                    my ($cg_count, $total_length, $cg_percentage) = calculate_cg_content($seq_data);
                    print "<tr><td>$current_header</td><td>$cg_count</td><td>$total_length</td><td>$cg_percentage%</td></tr>";
                    $seq_data = '';  # Reset for the next sequence
                }
                $current_header = $line;  # Store the header
            } else {
                # Concatenate the sequence data
                $seq_data .= $line;
            }
        }

        # Handle the last sequence after the file ends
        if ($seq_data) {
            my ($cg_count, $total_length, $cg_percentage) = calculate_cg_content($seq_data);
            print "<tr><td>$current_header</td><td>$cg_count</td><td>$total_length</td><td>$cg_percentage%</td></tr>";
        }

        print "</table></div>";
    } else {
        print "<div style='text-align: center;'><p>Error: Could not read the uploaded file.</p></div>";
    }
}

print end_html();

# Function to calculate CG content
sub calculate_cg_content {
    my ($sequence) = @_;
    my $cg_count = ($sequence =~ tr/CGcg//);  # Count C and G characters (both uppercase and lowercase)
    my $total_length = length($sequence);    # Total length of the sequence
    my $cg_percentage = sprintf("%.2f", ($cg_count / $total_length) * 100);  # Calculate percentage, rounded to 2 decimal places
    return ($cg_count, $total_length, $cg_percentage);
}

