import os
import pymsteams


class MsTeams:
    """Class to help organize the code"""

    def send_message(self, article):
        """Method to send a message using microsof teams connector webhook"""
        card = pymsteams.connectorcard(os.environ["MS_TEAMS_WEBHOOK_URL"])
        section = pymsteams.cardsection()
        section_html = f"""
<h2><em>Details</em></h2>
<p>{article["description"]}</p>
<br>
<img src={article["image_url"]} style="max-width:200px;width:100%""/>
"""
        section.text(section_html)
        card.addSection(section)
        section.addFact("Source:", article["source"])
        section.addFact("Author:", article["author"])
        section.addFact("Date Published:", article["publish_date"])
        card.addLinkButton("Read full story", article["url"])
        cves = []
        if "interesting" in article["tags"]:
            for item in article["tags"]["interesting"]:
                if "name" in item and item["name"] == "CVE's":
                    cves = item["values"]
        if len(cves) > 0:
            section.addFact("CVEs:", ", ".join(cves))
            for cve in cves:
                card.addLinkButton(cve, f"https://nvd.nist.gov/vuln/detail/{cve}")
        card.title(article["title"])
        card.summary(article["description"])
        assert card.send()
