import pymsteams
import os


class MsTeams:

    def send_message(self, article):
        card = pymsteams.connectorcard(os.environ["MS_TEAMS_WEBHOOK_URL"])
        section = pymsteams.cardsection()
        section_html = f"""
<h2>Description</h2>
<p>{article.description}</p>
<br>
<img src={article.image_url} style="max-width:200px;width:100%""/>
"""
        section.text(section_html)
        card.addSection(section)
        section.addFact("Source", article.source)
        section.addFact("Author", article.author)
        section.addFact("Date Published", article.publish_date)
        card.title(article.title)
        card.summary(f"{article.description}")
        card.addLinkButton("Read full story", article.url)
        assert card.send()
