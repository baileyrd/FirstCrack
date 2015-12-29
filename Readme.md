# First Crack #

### Introduction: ###
First Crack is a content management system, or CMS, that I began designing in late 2011 after learning of Marco Arment's plans to build his own CMS called "Second Crack". My choice of the name "First Crack" is simply a nod of acknowledgment to Marco's work, not necessarily an indication that I believe First Crack to be a superior service.  

First Crack is designed to be as easy to use as possible. Therefore, it does not require any knowledge of Python--the language I wrote First Crack in--or HTML, CSS, or Javascript to use. Simply save plaintext files, formatted using John Gruber's Markdown, to the "Content" directory, run Update.py, and open your updated site. Though it is designed not to require programing knowledge, I have also built First Crack to be as versatile as possible in the hopes of fitting as many needs as possible. Pursuant of that goal, every aspect of this CMS is customizable: if you find the default layout unsuitable, go ahead and change it by editing "Template.htm" located in the System folder buried within Structure. As long as your HTML is valid, the CMS will accept the changes as soon as a content file has been updated and apply them to the site.  

Despite my efforts to make this process as streamlined as possible, I acknowledge that publishing through my CMS could be simplified and improved. Therefore, if you have any suggestions, questions, comments, or concerns, feel free to contact me through my website, [zacjszewczyk.com](http://zacjszewczyk.com/), or on Twitter using the handle "@zacjszewczyk". Below I have provided a more in-depth explanation of the inner-workings of my CMS, as well as a short walkthrough to help you get up and running. Enjoy.  

---

### Directory Structure: ###
First, let's talk a bit about the directory structure: First Crack relies on a specific hierarchy in order to function. Within the root First Cack folder, you will find the following directory tree: Behavior; Content, and within it a folder named System; Structure, also containing a folder named System; Images, and Style. These folders contain the required Javascript files, content documents, HTML structure resources, the site's images, and the CSS governing the look and feel, respectively. Without this directory structure, First Crack cannot function. Thus, it is strongly recommended that you not change the location or names of these folders. However, the addition of new folders will not effect the performance of this CMS.  

### Types of Files: ###
In addition to being a bit particular about the names and locations of the directories, First Crack is also a bit exacting as to the types of files it accepts. Though it is not required, I recommend using the .js file extension for Javascript files and the .css extension for CSS files simply because it is good programming practice. First Crack does, however, require that content files be plaintext documents denoted by the .txt extension. Further, First Crack also assumes that all content documents are formatted with Markdown, which I will go talk about later. Finally, First Crack generates all HTML files to conform to the XHTML 1.0 Strict specification; HTML files are denoted with the .htm extension, rather than .html.  

### Markdown: ###
In the previous paragraph, I mentioned that in order for content files to be correctly parsed by First Crack, they must be plaintext files utilizing the .txt file extension, formatted with Markdown. From John Gruber's page on Markdown, "Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML)." For more information on Markdown, see [the documentation page](http://daringfireball.net/projects/markdown/) on Daringfireball.net. Before moving on though, I would like to provide a few basic instructions for writing in Markdown:  

Paragraphs, in Markdown, are formatted very similarly to the layout here: simply write a paragraph, then end it with two spaces (&nbsp;&nbsp;) following the last character. Italic text is denoted by surrounding a portion of text with asterisk (&#42;) marks: In this sentence, &#42;this text is italic.&#42; "this text is italic." would be italicized. Currently, First Crack does not support bold text. However, if the need presents itself, simply surround a portion of text with the HTML tags for bold, &#60;strong&#62; and &#60;/strong&#62;: In this sentence, &#60;strong&#62;this text is bold.&#60;/strong&#62; "this text is bold." would be displayed in bold text. To create a link in Markdown, use the following format: &#91;name of link as it should be displayed&#93;(url). As an example, take &#91;Google&#93;(http://www.google.com): this link would be parsed and printed to the page as &#60;a href="http://www.google.com"&#62;Google&#60;/a&#62;. Note that "http://www." must be past of the URL. Othwerwise, the CMS assumes that you are linking to a local file. With that, let's move on to block-level elements.  

In addition to inline elements such as the &#60;em&#62;, &#60;strong&#62;, and &#60;a&#62; tags denoting italic text, bold text, and links, respectively, Markdown also provides for the use of heading elements &#60;h1&#62; through &#60;h4&#62;. For those unfamiliar with heading elements, the &#60;h1&#62;-&#60;h6&#62; tags are generally used to separate a title or heading from a body of text. In Markdown, heading elements are designated by surrounding the desired header with a number of hash marks. The number of hash marks corresponds to the integer following the "h" in the header elements: "&#35; Header &#35;" results in &#60;h1&#62;Header&#60;/h1&#62;, "&#35;&#35; Header &#35;&#35;" results in &#60;h2&#62;Header&#60;/h2&#62;, and so on.  

--

### Making a Post: ###
Now that you are familiar with the directory structure, types of files First Crack requires, and have some understanding of markdown, the final section of this readme file will be to provide a brief tutorial on creating and publishing a post with First Crack.  

1. First, create a new text document and save it to the Content directory. Choose any name you desire, though I recommend it be similar to or the same as the title of the article it represents.  
2. Once the text document has been named and saved, open it in your favorite plaintext editor. I recommend Sublime Text.  
3. Place the title on the first line. To specify a title, surround the title with a single hash tag, signifying that it is an &#60;h1&#62; element. The result should look like this: "# Article Title #".  
4. Leave a blank line after the title, before the first paragraph. To start a paragraph, simply type the contents of the paragraph, then end it with two spaces. Repeat this step for as many paragraphs as you want to article to contain.
6. Save the document and run Update.py. Update.py will update the entire site to reflect the changes you have made. To view the new site, navigate to the Structure folder and open index.htm in your web browser. Congratulations, you have published your first article with First Crack.  

### Removing a Post: ###
To remove a post, simply delete the content file from the Content directory, then run Update.py. The CMS will remove the appropriate Structure file and rebuild  the site to reflect your changes.

---

### First Crack's Authoring Mode ###

First Crack also comes equipped with an "authoring" mode, which allows you to do the following: force a single article to rebuild, force all articles to rebuild, upload a specific article, upload the most recent five articles, re-upload the entire website, and upload all back-end files. Enter this mode by entering "./Update.py -a" at the command prompt, at which point the CMS will prompt you for further input.  