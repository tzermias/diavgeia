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
    unitIds = Field()
    signerIds = Field()
    thematicCategoryIds = Field()
    privateDate = Field()
    submissionTimestamp = Field()
    publishTimestamp = Field()
    status = Field()
    versionId= Field()
    documentChecksum = Field()
    attachments = Field()
    extraFieldValues = Field()
    correctedVersionId = Field()
    issueDate = Field()
    url = Field()
    documentUrl= Field()
    privateData = Field()

class Signer(Item):
    uid = Field()
    firstName = Field()
    lastName = Field()
    active = Field()
    activeFrom = Field()
    activeUntil = Field()
    organizationId = Field()
    hasOrganizationSignRights = Field()

class Unit(Item):
    uid = Field()
    label = Field()
    category = Field()
    active = Field()
    activeFrom = Field()
    parentId = Field()  
    
# vi: ts=4 sts=4 et sw=4 tw=80
