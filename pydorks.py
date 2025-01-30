import os
import platform
from urllib.parse import quote
from argparse import ArgumentParser, Namespace, ArgumentError

main_websites: dict = {
    'pythonwiki': 'wiki.python.org',
    'pythondocs': 'docs.python.org',
    'youtube': 'youtube.com',
    'github': 'github.com',
    'giters': 'giters.com',
    'linkedin': 'linkedin.com',
    'geeksforgeeks':'geeksforgeeks.org',
    'w3schools': 'w3schools.com',
    'stackoverflow': 'stackoverflow.com',
    'medium': 'medium.com',
    'X': 'x.com',
    'pinterest': 'pinterest.com',
    'reddit':'reddit.com',
    'facebook': 'facebook.com',
    'instagram':'instagram.com'
}

def logo() -> None:
    print("""
            ██████╗ ██╗   ██╗██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗
            ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝
            ██████╔╝ ╚████╔╝ ██║  ██║██║   ██║██████╔╝█████╔╝ ███████╗
            ██╔═══╝   ╚██╔╝  ██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚════██║
            ██║        ██║   ██████╔╝╚██████╔╝██║  ██║██║  ██╗███████║
            ╚═╝        ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                            
            A simple command-line tool for automating search on Google.
            \n""")

def siteDescription() -> str:
    sites: str ='The list of sites your results will depend on. (multiple choices seperated by ",").\n'
    sites+='When choosing the option all, the results will be based on the following list: linkedin.com,\n'
    for url in main_websites.values():
        sites+=f'\t{url}\n'
    return sites

parser = ArgumentParser(
    description=logo(), 
    usage='pydorks [query ...] [-h] [-w [WORD]] [-n [NOTWORD]] [-i [INTEXT ...]] [-u [INURL]] [-a [ALLINURL ...]] [-s [SITES]]'
)
parser.add_argument('query', help='The keywords and/or phrases you want to search for.', type=str, nargs='*')
parser.add_argument('-w', '--word', help='Show results with this word exactly. Do not include similar words. ', type=str, nargs='?')
parser.add_argument('-n', '--notword', help='Do not include this word in search results or queries.', type=str, nargs='?')
parser.add_argument('-e', '--intext', help='Search the body of the webpage for specific text.', type=str, nargs='*')
parser.add_argument('-i', '--intitle', help='search within the title of a webpage for specific keywords or phrases.', type=str, nargs='*')
parser.add_argument('-u', '--inurl', help='Value is contained somewhere in the url.', type=str, nargs='?')
parser.add_argument('-a','--allinurl', help='Search all of the following words in the url.', type=str, nargs='*')
parser.add_argument('-f', '--filetype', help='Search only for files, not webpages.', type=str, nargs='?')
parser.add_argument('-r', '--related', help='Find website results that are related to your search term.', type=str, nargs='?')
parser.add_argument('-o', '--info', help='Find supplemental information Google may have on this page. ( useful for finding cached pages )', type=str, nargs='?')
parser.add_argument('-l', '--link', help='Find other pages indexed by Google that reference this link.', type=str, nargs='?')  
parser.add_argument('-s', '--sites', help=siteDescription(), type=str, nargs='?', default='google')


try:
    args: Namespace = parser.parse_args()
except ArgumentError as err:
        print(str(err))
        parser.print_help() 
        exit(1)

###### including word filter object #######
class WordFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def words_filter(self) -> str:
        if args.word:
            self.filter +=  f' +{args.word} '
        
        return self.filter
    
    
###### Excluding word filter object #######
class NotWordFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def notwords_filter(self) -> str:
        if args.notword:
            self.filter +=  f' -{args.notword} '
        
        return self.filter
    

###### In url filter object #######
class InUrlFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def inurl_filter(self) -> str:
        if args.inurl:
            self.filter +=  f' inurl:{args.inurl} '
        
        return self.filter
    
    
###### All in url filter object #######
class AllInUrlFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def allinurl_filter(self) -> str:
        if args.allinurl:
            self.filter +=  ' allinurl:"'
            for word in args.allinurl:
                self.filter += word + ' '
            self.filter += '" ' 
        
        return self.filter
    
    
###### In text filter object #######
class InTextFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def intext_filter(self) -> str:
        if args.intext:
            self.filter +=  ' intext:"'
            for word in args.intext:
                self.filter += word + ' ' 
            self.filter += '" ' 
        
        return self.filter
    

###### In title filter object #######
class InTitleFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def intitle_filter(self) -> str:
        if args.intitle:
            self.filter: str =  f' intitle:"{args.intitle}" '
        
        return self.filter
    
    
###### Filetype filter object #######
class FileTypeFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def filetype_filter(self) -> str:
        if args.filetype:
            self.filter +=  f' filetype:{args.filetype} '
        
        return self.filter

    
###### related filter object ######
class RelatedFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def related_filter(self) -> str:
        if args.related:
            self.filter +=  f' related:"{args.related}" '
        
        return self.filter
    
    
###### Info filter object #######
class InfoFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def info_filter(self) -> str:
        if args.info:
            self.filter +=  f' info:"{args.info}" '
        
        return self.filter
    
    
###### Link filter object #######
class LinkFilter:
    def __init__(self) -> None:
        self.filter: str = ''
    
    def link_filter(self) -> str:
        if args.link:
            self.filter +=  f' link:"{args.link}" '
        
        return self.filter
    

###### Sites filter object #######
class SiteFilter:

    def __init__(self) -> None:
        self.filter: str = ' ( '

    def sites_default(self) -> str:
        return ''
    
    def sites_all(self) -> str:
        for index, value in enumerate(main_websites):
            self.filter += "site:" + main_websites[value]
            if index != len(main_websites) - 1:
                self.filter += " OR "
            else:
                self.filter += " ) "
        return self.filter
    
    def sites_selected(self) -> str:
        wanted_sites = args.sites.split(',')
        for index, site in enumerate(wanted_sites):
            self.filter += "site:*." + site + ".*"
            if index != len(wanted_sites) - 1:
                self.filter += " OR "
        self.filter += " ) "
        return self.filter


#### __name__ = __main__ ####
def main() -> None:
    query: str = args.query
    query = ' '.join(query)
    if query == "":
        os.system('start https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    else:
        if args.sites == 'google':
            site_filter: str = SiteFilter().sites_default()
        elif args.sites == 'all':
            site_filter: str = SiteFilter().sites_all()
        else:
            site_filter: str = SiteFilter().sites_selected()

        word: str = WordFilter().words_filter()
        notword: str = NotWordFilter().notwords_filter()
        inurl: str = InUrlFilter().inurl_filter()
        allinurl: str = AllInUrlFilter().allinurl_filter()
        intext: str = InTextFilter().intext_filter()
        intitle: str = InTitleFilter().intitle_filter()
        related: str = RelatedFilter().related_filter()
        info: str = InfoFilter().info_filter()
        link: str = LinkFilter().link_filter()

        parsed_query: str = quote(query + word + notword + intext + intitle + inurl + allinurl + related + info + link + site_filter)
        url: str = "https://www.google.com/search?q=" + parsed_query

        system: str = platform.system()

        if system == 'Windows':
            os.system(f'start {url}')
        elif system == 'Linux':
            os.system(f'xdg-open "{url}"')
        elif system == 'Macos':
            os.system(f'open "{url}"')

if __name__ == '__main__':
    main()
