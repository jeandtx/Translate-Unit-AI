"""DECLARE SCHEMAS HERE"""

import google.generativeai as genai

source_item = genai.protos.Schema(
    description="Item from the image to translate from",
    type=genai.protos.Type.OBJECT,
    properties={
        "unit": genai.protos.Schema(
            description="The unit to translate from", type=genai.protos.Type.STRING
        ),
        "value": genai.protos.Schema(
            description="The value to translate", type=genai.protos.Type.NUMBER
        ),
    },
    required=["unit", "value"],
)

target_item = genai.protos.Schema(
    description="Item after translation.",
    type=genai.protos.Type.OBJECT,
    properties={
        "unit": genai.protos.Schema(
            description="The unit to translate to", type=genai.protos.Type.STRING
        ),
        "value": genai.protos.Schema(
            description="The value after translation", type=genai.protos.Type.NUMBER
        ),
    },
    required=["unit", "value"],
)

price = genai.protos.Schema(
    description="Price object. Always provide both source and target objects.",
    type=genai.protos.Type.OBJECT,
    properties={
        "source": source_item,
        "target": target_item,
    },
    required=["source", "target"],
)

price_list = genai.protos.Schema(
    description="Array of all price translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=price,
    nullable=True,
)

distance = genai.protos.Schema(
    description="Distance object",
    type=genai.protos.Type.OBJECT,
    properties={"source": source_item, "target": target_item},
    required=["source", "target"],
)

distance_list = genai.protos.Schema(
    description="Array of all distance translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=distance,
    nullable=True,
)

weight = genai.protos.Schema(
    description="Weight object",
    type=genai.protos.Type.OBJECT,
    properties={
        "source": source_item,
        "target": target_item,
    },
    required=["source", "target"],
)

weight_list = genai.protos.Schema(
    description="Array of all weight translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=weight,
    nullable=True,
)

length = genai.protos.Schema(
    description="Length object",
    type=genai.protos.Type.OBJECT,
    properties={"source": source_item, "target": target_item},
    required=["source", "target"],
)

length_list = genai.protos.Schema(
    description="Array of all length translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=length,
    nullable=True,
)

volume = genai.protos.Schema(
    description="Volume object",
    type=genai.protos.Type.OBJECT,
    properties={"source": source_item, "target": target_item},
    required=["source", "target"],
)

volume_list = genai.protos.Schema(
    description="Array of all volume translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=volume,
    nullable=True,
)

temperature = genai.protos.Schema(
    description="Temperature object",
    type=genai.protos.Type.OBJECT,
    properties={
        "source": source_item,
        "target": target_item,
    },
    required=["source", "target"],
)

temperature_list = genai.protos.Schema(
    description="Array of all temperature translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=temperature,
    nullable=True,
)

area = genai.protos.Schema(
    description="Area object",
    type=genai.protos.Type.OBJECT,
    properties={
        "source": source_item,
        "target": target_item,
    },
    required=["source", "target"],
)

area_list = genai.protos.Schema(
    description="Array of all area translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=area,
    nullable=True,
)

speed = genai.protos.Schema(
    description="Speed object",
    type=genai.protos.Type.OBJECT,
    properties={
        "source": source_item,
        "target": target_item,
    },
    required=["source", "target"],
)

speed_list = genai.protos.Schema(
    description="Array of all speed translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=speed,
    nullable=True,
)

footwear = genai.protos.Schema(
    description="Footwear object",
    type=genai.protos.Type.OBJECT,
    properties={
        "source": source_item,
        "target": target_item,
    },
    required=["source", "target"],
)

footwear_list = genai.protos.Schema(
    description="Array of all footwear translations detected in the image",
    type=genai.protos.Type.ARRAY,
    items=footwear,
    nullable=True,
)

translate = genai.protos.FunctionDeclaration(
    name="translate",
    description="Translate the units in the image",
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            "prices": price_list,
            "distances": distance_list,
            "weights": weight_list,
            "lengths": length_list,
            "volumes": volume_list,
            "temperatures": temperature_list,
            "areas": area_list,
            "speeds": speed_list,
            "footwears": footwear_list,
        },
    ),
)
