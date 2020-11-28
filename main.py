import click
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
from config import URL, DISPLAY_OPTIONS
from Scraper import Scraper


def validate_format(ctx, param, value):
    try:
        selections = value.lower().split(",") if value != ("all") else value
        if param.name == "authors" and value != ("all"):
            selections = list(map(lambda n: n.lower().replace("_", " "), selections))
        elif param.name == "months" and value != ("all"):
            for selection in selections:
                if not selection.isdigit() or int(selection) > 12 or int(selection) < 1: raise ValueError("Month "
                                                                                                          "selection \""
                                                                                                          + str(
                    selection) + "\" is not valid. Please choose numbers between 1 and 12")
        elif param.name == "display" and value != ("all"):
            for selection in selections:
                if selection not in DISPLAY_OPTIONS:
                    raise ValueError(
                        "Display option \"" + str(selection) + "\" not available, please choose from " + str(
                            DISPLAY_OPTIONS))
        return selections
    except ValueError as e:
        print("Option not properly formatted. Please run python3 Scraper.py --help to check usage")
        raise click.BadParameter(e)


@click.command()
@click.option('--tags', default=("all"), callback=validate_format, help='Option to scrape subset of tags (separated '
                                                                        'by commas, no spaces). Default: all\n '
                                                                        'Example: python3 '
                                                                        'Scraper.py --tags=gaming,fintech \n')
@click.option('--authors', default=("all"), callback=validate_format, help='Option to scrape subset of authors ('
                                                                           'format: name_lastname separated by commas, '
                                                                           'no spaces). Default: all\nExample: python3 '
                                                                           'Scraper.py '
                                                                           '--authors=Julian_Willson,Martha_Janes\n')
@click.option('--today', default=False, help='Option to scrape only todays articles. Default:False \n Example: '
                                             'python3 Scraper.py '
                                             '--today=True \n')
@click.option('--months', default=("all"), callback=validate_format, help='Option to scrape only articles from '
                                                                          'specified months(separated by commas, '
                                                                          'no spaces) Default: all\nExample: python3 '
                                                                          'Scraper.py --months=1 \n')
@click.option('--display', default=("all"), callback=validate_format, help='Option to select information to display '
                                                                           'from '
                                                                           'tags, title, author, twitter, date ('
                                                                           'separated by commas, no spaces) '
                                                                           'Default: all\n'
                                                                           'Example: python3 Scraper.py '
                                                                           '--display=tags,title \n')
@click.option('--limit', default=None, type=int, help='Option to limit number of articles. Default: None \nExample: '
                                                      '--limit=250')

def main(tags, authors, months, display, today, limit):
    print_params = tuple(
        map(lambda p: ', '.join(p) if isinstance(p, tuple) else p, (tags, authors, months, today, display, str(limit))))
    click.echo(f"Initalizing Techcrunch Webscraper... Currently scraping for: %s tags, %s authors, months number %s . "
               f"\nScraping only today's articles: %s.\nWill display %s information for articles\nArticle limit: %s" % print_params)

    tc_scraper = Scraper(tags, authors, months, display, today, limit)

    try:
        tc_scraper.scrape()
    except NoSuchWindowException as e:
        print("Error: Window not found. Make sure scraping browser was not closed", e)


if __name__ == '__main__':
    main()
