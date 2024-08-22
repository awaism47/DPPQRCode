from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl

# Model for nested 'ValueUnit' fields
class ValueUnit(BaseModel):
    value: float
    unit: str

# Model for nested 'KeyValue' fields
class KeyValue(BaseModel):
    value: str
    key: str

# Model for metadata section
class Metadata(BaseModel):
    backupReference: HttpUrl
    registrationIdentifier: HttpUrl
    economicOperatorId: str
    lastModification: str
    predecessor: str
    issueDate: str
    version: str
    passportIdentifier: str
    status: str
    expirationDate: str

# Model for characteristics section
class PhysicalDimension(BaseModel):
    volume: ValueUnit
    grossWeight: ValueUnit
    diameter: ValueUnit
    grossVolume: ValueUnit
    width: ValueUnit
    length: ValueUnit
    weight: ValueUnit
    height: ValueUnit

class Lifespan(BaseModel):
    value: int
    unit: str
    key: str

class Characteristics(BaseModel):
    generalPerformanceClass: str
    physicalState: str
    physicalDimension: PhysicalDimension
    lifespan: List[Lifespan]

# Model for commercial section
class Commercial(BaseModel):
    placedOnMarket: str
    purpose: List[str]

# Model for identification section
class TypeIdentification(BaseModel):
    manufacturerPartId: str
    nameAtManufacturer: str

class Classification(BaseModel):
    classificationStandard: str
    classificationID: str
    classificationDescription: str

class DataCarrier(BaseModel):
    carrierType: str
    carrierLayout: str

class Identification(BaseModel):
    batch: List[KeyValue]
    codes: List[KeyValue]
    type: TypeIdentification
    classification: List[Classification]
    serial: List[KeyValue]
    dataCarrier: DataCarrier

# Model for sources section
class Source(BaseModel):
    header: str
    category: str
    type: str
    content: HttpUrl

# Model for materials section
class HazardClassification(BaseModel):
    category: str
    statement: str
    class_: str

class Documentation(BaseModel):
    contentType: str
    header: str
    content: HttpUrl

class ConcentrationRange(BaseModel):
    max: float
    min: float

class Id(BaseModel):
    type: str
    name: str
    id: str

class SubstancesOfConcernContent(BaseModel):
    unit: str
    hazardClassification: HazardClassification
    documentation: List[Documentation]
    concentrationRange: List[ConcentrationRange]
    location: str
    concentration: float
    exemption: str
    id: List[Id]

class MaterialCompositionContent(BaseModel):
    unit: str
    recycled: float
    critical: bool
    renewable: float
    documentation: List[Documentation]
    concentration: float
    id: List[Id]

class SubstancesOfConcern(BaseModel):
    applicable: bool
    content: List[SubstancesOfConcernContent]

class MaterialComposition(BaseModel):
    applicable: bool
    content: List[MaterialCompositionContent]

class Materials(BaseModel):
    substancesOfConcern: SubstancesOfConcern
    materialComposition: MaterialComposition

# Model for handling section
class HandlingContent(BaseModel):
    producer: List[KeyValue]
    sparePart: List[TypeIdentification]

class Handling(BaseModel):
    applicable: bool
    content: HandlingContent

# Model for additional data section
class AdditionalDataType(BaseModel):
    typeUnit: str
    dataType: str

class AdditionalDataChildren(BaseModel):
    description: str
    label: str
    type: AdditionalDataType
    data: str

class AdditionalData(BaseModel):
    description: str
    label: str
    type: AdditionalDataType
    data: str
    children: Optional[List[AdditionalDataChildren]]

# Model for operation section
class ImportContent(BaseModel):
    eori: str
    id: str

class OperationImport(BaseModel):
    applicable: bool
    content: ImportContent

class OperationOther(BaseModel):
    id: str
    role: str

class OperationManufacturerFacility(BaseModel):
    facility: str

class OperationManufacturer(BaseModel):
    facility: List[OperationManufacturerFacility]
    manufacturingDate: str
    manufacturer: str

class Operation(BaseModel):
    import_: OperationImport
    other: OperationOther
    manufacturer: OperationManufacturer

# Model for sustainability section
class ProductFootprintContent(BaseModel):
    lifecycle: str
    rulebook: List[Documentation]
    unit: str
    performanceClass: str
    manufacturingPlant: List[OperationManufacturerFacility]
    type: str
    value: float
    declaration: List[Documentation]

class ProductFootprint(BaseModel):
    material: List[ProductFootprintContent]
    carbon: List[ProductFootprintContent]
    environmental: List[ProductFootprintContent]

class Sustainability(BaseModel):
    reparabilityScore: str
    productFootprint: ProductFootprint
    status: str
    durabilityScore: str


# The main model for Digital Product Passport
class DigitalProductPassport1(BaseModel):
    metadata: Optional[str] = None
    characteristics: Optional[str] = None
    commercial: Optional[str] = None
    identification: Optional[str] = None
    sources: Optional[str] = None
    materials: Optional[str] = None
    handling: Optional[str] = None
    additionalData: Optional[str] = None
    operation: Optional[str] = None
    sustainability: Optional[str] = None

print("DigitalProductPassport model loaded")
