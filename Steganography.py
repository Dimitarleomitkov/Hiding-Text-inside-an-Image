from PIL import Image
from PIL import ImageColor
import binascii
import optparse

# function to take rgb values and convert them to hex
def rgb2hex (r, g, b):
	return "#{:02x}{:02x}{:02x}".format (r, g, b);

# function to take hex values and convert them to rgb
def hex2rgb (hexcode):
	return ImageColor.getcolor (hexcode, "RGB");

# function to take a string and convert it to binary
def str2bin (message):
	binary = "".join (format (ord (i), "08b") for i in message);
	return binary; 

# function to take a binary and convert it to string
def bin2str (binary):
	string = "";

	for i in range (0, len (binary), 8):
		temp_data = binary[i : i + 8];
		decimal_data = int (temp_data, 2);
		string = string + chr (decimal_data);

	return string;

# function to encode the last bit of a color
def encode (hexcode, digit):
	if (hexcode[-1] in ('0', '1', '2', '3', '4', '5')):
		hexcode = hexcode[:-1] + digit;
		return hexcode;
	else:
		return None;

# function to decode the last bit of a color
def decode (hexcode):
	if (hexcode[-1] in ('0', '1')):
		return hexcode[-1];
	else:
		return None;

# function to hide a message
def hide (filename, message):
	# Create an image files
	img = Image.open (filename);
	# Convert the message into binary and add the end flag for the message
	binary = str2bin (message) + "1111111111111110";

	# Make sure the image is in the right format
	if (img.mode in ('RGBA')):
		img = img.convert ('RGBA');
		# Return all the pixels inside the image
		datas = img.getdata ();

		newData = [];
		codeBit = 0;
		temp = '';

		# For each pixel in the image
		for item in datas:
			if (codeBit < len (binary)):
				# Encode our data into the pixel
				newpix = encode (rgb2hex (item[0], item[1], item[2]), binary[codeBit]);
				# If it failed stay with the same pixel
				if (newpix == None):
					newData.append (item);
				else:
					# Convert the new rgb value into hex
					r, g, b = hex2rgb (newpix);
					# Store the new pixel
					newData.append ((r,g,b,255));
					# Increment how many symbols have been hidden
					codeBit = codeBit + 1;
			else:
				newData.append (item);
		# Create the new image
		img.putdata (newData);
		# Save the new image
		img.save ("EncodedImage.jpg", "PNG");

		return "Encoding done.";
	else:
		return "Incorrect image mode.";

# function to retreive a message from the image
def retrieve (filename):
	# Open an image file
	img = Image.open (filename);
	# Save the binary in a variable
	binary = '';

	# Make sure the image is in the right format
	if (img.mode in ('RGBA')):
		img = img.convert ('RGBA');
		data_buff = img.getdata ();
		
		# For each pixel in the image
		for item in data_buff:
			# Get the encoded bit out
			bit = decode (rgb2hex (item[0], item[1], item[2]));
			if (bit == None):
				pass;
			else:
				binary = binary + bit;
				# Check for the end
				if (binary[-16:] == '1111111111111110'):
					print ("Message found.");
					# return the message
					return bin2str (binary[:-16]);

		return bin2str (binary);
	else:
		return "Incorrect image mode.";

def Main ():
	# Parsing the input of the program from the command line when calling the script
	parser = optparse.OptionParser ("usage %prog " + "-e/-d <target file>");
	# Implement the option for -e
	parser.add_option ("-e", dest = "hide", type = "string", help = "target picture path to hide text");
	# Implement the option for -d
	parser.add_option ("-d", dest = "retrieve", type = "string", help = "target picture path to retrieve text");

	(options, args) = parser.parse_args ();

	if (options.hide != None):
		text = input ("Enter a message to hide:");
		print (hide (options.hide, text));
	elif (options.retrieve != None):
		print (retrieve (options.retrieve));
	else:
		print (parser.usage);
		exit (0);

if __name__ == "__main__":
	Main ();