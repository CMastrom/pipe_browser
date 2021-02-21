import requests
from lxml import html as xml
from colors import Msg
import urllib.request as ureq
import os
# Req -> lxml
# Req -> requests

target_dir = os.path.dirname(__file__)+"/pics"
#BOB WAS HERE
help = f"""
	get(url) -> returns the website
		site = "" -> current site
		res = req.content -> content returned from the request (Same thing as request.content)
		html_content = html(req.content) -> converted DOM tree of the HTML
	links(append="") -> prints all links in website given the request content (Optional: pass a string to append to xpath)
		href = [] -> list of gathered hrefs
		href_label = [] -> list of gathered href labels
	html(request_content) -> returns request content converted to html tree
	inputs(append="", verbosity=-1) -> prints all inputs in the website given the request content (Optional: pass a string to append to the xpath) (Optional: pass verbosity of 'frisk', 'abuse', or 'beatdown' in order to get verbose, more verbose, or most verbose responses)
		_inputs = [] -> list of gathered inputs
		inputs_label = [] -> list of gathered input values
	imgs(append="") -> prints all images from the website given the request content (Optional: pass a string to append to the xpath)
		images = [] -> list of gathered image URLs
		images_alt = [] -> list of gathered image alts
	download(url, download_filename=False) -> downloads an image from the site given the URL (Optional: You can provide what you would like the file to be named once downloaded)
		target_dir = "{target_dir}" -> where images will be downloaded to (you can change this to any valid directory)
	pprint(html_element) -> pretty prints html given an element
		all = True -> can be passed into pprint() as html_element and pprint() will print all html
	scripts(append="", verbosity=-1) -> prints all <script>s from website
		_scripts = [] -> list of gathered script elements
		scripts_src = [] -> list of gathered script src
	metas(append="", verbosity=-1) -> prints all <meta>s from website
		_metas = [] -> list of gathered meta elements
		metas_content = [] -> list of gathered meta contents
	bitchdetector(verbosity=frisk) -> Uses these other methods collectively to analyze a given website. Verbosity can be 'frisk' (level 1 verbosity), 'abuse' (level 2 verbosity), or 'beatdown' (level 3 verbosity)
		frisk = 1
		abuse = 2
		beatdown = 3
"""

# metas
_metas = []
metas_content = []

# scripts
_scripts = []
scripts_src = []

# links
href = []
href_label = []

# inputs
_inputs = []
inputs_label = []

# imgs
images = []
images_alt = []

site = ""
res = ""
html_content = ""

# bitchdetector
frisk = 1
abuse = 2
beatdown = 3

# pprint
all = True

def get(url):
	global site, res, html_content
	site = url
	req = requests.get(url)
	if req.status_code == 200:
		print(Msg.fnote("STATUS")+"200")
	else:
		print(Msg.ferror("STATUS")+str(req.status_code))
	res = req.content
	html_content = html(req.content)
	return req

def html(request_content):
	return xml.fromstring(request_content)

def links(append=""):
	global href, href_label
	href.clear()
	href_label.clear()
	a_tags = html_content.xpath("//a"+append)
	a_tags.append(html_content.xpath("//button"))
	if not a_tags:
		print(Msg.fnote("NONE")+" Found none")
	for (index,link) in enumerate(a_tags):
		try:
			href.append(str(link.attrib['href']))
		except:
			href.append("No href found (or threw error)")
		try:
			href_label.append(str(link.text))
		except:
			href_label.append("No label found (or threw error)")
		print(Msg.fpurp("HREF")+ href_label[index] + " -> " + href[index] + " -> " + str(index))

def inputs(append="", verbosity=-1):
	global _inputs, inputs_label
	_inputs.clear()
	inputs_label.clear()
	input_tags = html_content.xpath("//input"+append)
	if not input_tags:
		print(Msg.fnote("NONE")+" Found none")
	for (index,_input) in enumerate(input_tags):
		try:
			_inputs.append(_input)
		except:
			_inputs.append("No input found (or threw error)")
		try:
			inputs_label.append(str(_input.value))
		except:
			inputs_label.append("No value found (or threw error)")
		print(Msg.fcyan("INPUT")+ inputs_label[index] + " -> " + str(_inputs[index]) + " -> " + str(index))
		if verbosity == abuse:
			pprint(_input)
			print("\t"+Msg.fnote("FINDING NAME")+"\t\t")
			try:
				print("\t\t"+Msg.fwarn("NAME")+_input.attrib['name'])
			except Exception:
				print("\t\t"+Msg.ferror("NO NAME")+" No name found")
			print("\n\t"+Msg.fnote("FINDING VALUE")+"\t\t")
			try:
				print("\t\t"+Msg.fwarn("VALUE")+_input.attrib['value']+"\n")
			except Exception:
				print("\t\t"+Msg.ferror("NO VALUE")+" No value found\n")

def imgs(append=""):
	global images, images_alt
	images.clear()
	images_alt.clear()
	image_tags = html_content.xpath("//img"+append)
	if not image_tags:
		print(Msg.fnote("NONE")+" Found none")
	for (index,image) in enumerate(image_tags):
		try:
			images.append(str(image.attrib['src']))
		except:
			images.append("No input found (or threw error)")
		try:
			images_alt.append(str(image.attrib['alt']))
		except:
			images_alt.append("No value found (or threw error)")
		print(Msg.fwarn("IMG")+ images_alt[index] + " -> " + images[index] + " -> " + str(index))

def scripts(append="", verbosity=-1):
	global _scripts, scripts_src
	_scripts.clear()
	scripts_src.clear()
	script_tags = html_content.xpath("//script"+append)
	if not script_tags:
		print(Msg.fnote("NONE")+" Found none")
	for (index,script) in enumerate(script_tags):
		try:
			_scripts.append(script)
		except:
			_scripts.append("No input found (or threw error)")
		try:
			scripts_src.append(str(script.attrib['src']))
		except:
			if verbosity == abuse:
				try:
					print(Msg.fcyan("DUMPING SCRIPT")+ " Script contents: \n\t")
					pprint(script)
					print("")
				except Exception:
					print(Msg.ferror("ERROR")+" Failed to dump script contents")
			scripts_src.append("No value found (or threw error)")
		print(Msg.ferror("SCRIPT")+ scripts_src[index] + " -> " + str(_scripts[index]) + " -> " + str(index))

def metas(append="", verbosity=-1):
	global _metas, metas_content
	_metas.clear()
	metas_content.clear()
	meta_tags = html_content.xpath("//meta"+append)
	if not meta_tags:
		print(Msg.fnote("NONE")+" Found none")
	for (index,meta) in enumerate(meta_tags):
		try:
			_metas.append(meta)
		except:
			_metas.append("No input found (or threw error)")
		try:
			metas_content.append(str(meta.attrib['content']))
		except:
			metas_content.append("No value found (or threw error)")
		print(Msg.ferror("META")+ metas_content[index] + " -> " + str(_metas[index]) + " -> " + str(index))
		if verbosity == abuse:
			pprint(meta)
			print("\t"+Msg.fnote("FINDING PROPERTY")+"\t\t")
			try:
				print("\t\t"+Msg.fwarn("PROPERTY")+meta.attrib['property'])
			except Exception:
				print("\t\t"+Msg.ferror("NO PROPERTY")+" No property found")
			print("\n\t"+Msg.fnote("FINDING NAME")+"\t\t")
			try:
				print("\t\t"+Msg.fwarn("NAME")+meta.attrib['name'])
			except Exception:
				print("\t\t"+Msg.ferror("NO NAME")+" No name found")
			print("\n\t"+Msg.fnote("FINDING ITEMPROP")+"\t\t")
			try:
				print("\t\t"+Msg.fwarn("ITEMPROP")+meta.attrib['itemprop']+"\n")
			except Exception:
				print("\t\t"+Msg.ferror("NO ITEMPROP")+" No itemprop found\n")

def download(url, download_filename=False):
	if not download_filename:
		download_filename = url.split('/')[-1]
	ureq.urlretrieve(url, target_dir+"/"+download_filename)
	# Check if download worked:
	if os.path.isfile(target_dir+"/"+download_filename):
		print(Msg.fsucc("DOWNLOAD COMPLETE")+"File '"+target_dir+"/"+download_filename+"' downloaded successfully.")
	else:
		print(Msg.ferror("DOWNLOAD FAILED")+" Failed to download file.")

def pprint(html_element):
	if html_element == all:
		print(xml.etree.tostring(html(res), encoding='unicode', pretty_print=True))
	else:
		print(xml.etree.tostring(html_element, encoding='unicode', pretty_print=True))

def bitchdetector(verbosity=frisk):
	if verbosity == frisk:
		print(Msg.fcyan("BitchDetector")+": Frisking target (level 1): ")
		print(Msg.fnote("SCRIPTS")+" Finding all JS scripts the target would like to run...")
		print(scripts())
		print("\n"+Msg.fnote("METAS")+" Finding all embedded meta data tags that the target uses...")
		print(metas())
		print("\n"+Msg.fnote("INPUTS")+" Finding all hidden inputs that the target is hiding...")
		print(inputs("[contains(@type, 'hidden')]"))
	elif verbosity == abuse:
		print(Msg.fcyan("BitchDetector")+": Abusing target (level 2): ")
		print(Msg.fnote("SCRIPTS")+" Finding all JS scripts the target would like to run...")
		print(scripts(verbosity=abuse))
		print("\n"+Msg.fnote("METAS")+" Finding all embedded meta data tags that the target uses...")
		print(metas(verbosity=abuse))		
		print("\n"+Msg.fnote("INPUTS")+" Finding all hidden inputs that the target is hiding...")
		print(inputs("[contains(@type, 'hidden')]", verbosity=abuse))
				
	#elif verbosity == beatdown:

	else:
		print(Msg.ferror("ERROR")+" Verbosity '"+verbosity+"' not recognized. Must be 'frisk' (level 1), 'abuse' (level 2), or 'beatdown' (level 3).")
