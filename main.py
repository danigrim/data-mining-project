"""
File initializes program and CLI
Authors: Daniella Grimberg & Eddie Mattout
"""

import click
from config import URL, DISPLAY_OPTIONS
from Orchestrator import Orchestrator


def validate_format(ctx, param, value):
    """
    Function validates format of user input for CLI parameters
    :param ctx:
    :param param: parameter being validated
    :param value: user inputted value (or default)
    :return:
    """
    try:
        selections = value.lower().split(",") if value != "all" else value  # make into a list and take lowercase
        if param.name == "authors" and value != "all":
            selections = list(map(lambda n: n.lower().replace("_", " "), selections))  # reformat author full name
        elif param.name == "months" and value != "all":
            for selection in selections:
                if not selection.isdigit() or int(selection) > 12 or int(selection) < 1: raise ValueError("Month "
                                                                                                          "selection "
                                                                                                          "" + str(
                    selection) + "\" is not valid. Please choose numbers between 1 and 12")
        elif param.name == "display" and value != "all":
            for selection in selections:
                if selection not in DISPLAY_OPTIONS:
                    raise ValueError(
                        "Display option \"" + str(selection) + "\" not available, please choose from " + str(
                            DISPLAY_OPTIONS))
        return selections
    except ValueError as e:
        print("Option not properly formatted. Please run python3 main.py --help to check usage")
        raise click.BadParameter(e)


@click.command()
@click.option('--tags', default="all", callback=validate_format, help='Option to scrape subset of tags (separated '
                                                                      'by commas, no spaces). Default: all\n '
                                                                      'Example: python3 '
                                                                      'main.py --tags=gaming,fintech \n')
@click.option('--authors', default="all", callback=validate_format, help='Option to scrape subset of authors ('
                                                                         'format: name_lastname separated by commas, '
                                                                         'no spaces). Default: all\nExample: python3 '
                                                                         'main.py '
                                                                         '--authors=Julian_Willson,Martha_Janes\n')
@click.option('--today', default=False, type=bool,
              help='Option to scrape only todays articles. Default:False \n Example: '
                   'python3 main.py '
                   '--today=True \n')
@click.option('--months', default="all", callback=validate_format, help='Option to scrape only articles from '
                                                                        'specified months(number indexes separated by'
                                                                        'commas, no spaces) Default: all\nExample: '
                                                                        'python3 main.py --months=1,2 \n')
@click.option('--display', default="all", callback=validate_format, help='Option to select information to display '
                                                                         'from '
                                                                         'tags, title, author, twitter, date, count ('
                                                                         'separated by commas, no spaces) '
                                                                         'Default: all\n'
                                                                         'Example: python3 main.py '
                                                                         '--display=tags,title \n')
@click.option('--limit', default=None, type=int, help='Option to limit number of articles. Default: None \nExample: '
                                                      '--limit=250')
@click.option('--make_db', default=False, type=bool, help='Option to initialize database and create necessary tables. '
                                                          'set to True in first time running scraper. '
                                                          'Example: python3 main.py --make_db=True ')
def main(tags, authors, months, display, today, limit, make_db):
    """
    Main function used to take in user arguments (scraping preferences) and initialize the scraper
    :param tags:user list of tags to scrape for
    :param authors: user list of authors looking for
    :param months: user list of months by index ex january and february 1,2
    :param display: user list of preferences for what will be displayed
    :param today: Boolean to indicate if to only scrape todays articles
    :param make_db: True if need to make
    :param limit: (int) limit of iterations
    :return:
    """
    print_params = tuple(
        map(lambda p: ', '.join(p) if isinstance(p, tuple) else p, (tags, authors, months, today, display, str(limit))))
    click.echo(f"Initializing Techcrunch scraper... Currently scraping for: %s tags, %s authors, months: %s . "
               f"\nScraping only today's articles: %s.\nWill display %s information for articles\nArticle limit: %s" %
               print_params)
    orchestrator = Orchestrator(tags, authors, months, display, today, limit, make_db)
    orchestrator.run()


if __name__ == '__main__':
    main()
