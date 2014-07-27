#
# items.py
#
# Define the structure of a DiavgeiaItem

from scrapy.item import Item, Field

class DiavgeiaItem(Item):
    ada = Field()
    protocolNumber = Field()
    subject = Field()
    decisionTypeId = Field()
    organizationId = Field()
    #unitIds = Field()
    signerIds = Field()
    thematicCategoryIds = Field()
    privateDate = Field()
    submissionTimestamp = Field()
    status = Field()
    versionId= Field()
    documentChecksum = Field()
    #attachments = Field()
    #extraFieldValues = Field()
    correctedVersionId = Field()
    issueDate = Field()
    url = Field()
    documentUrl= Field()
    privateData = Field()

    
# vi: ts=4 sts=4 et sw=4 tw=80
