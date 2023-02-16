payload_config_schema = {
  "type": "object",
  "required": ["reference", "lab"],
  "properties": {
    "reference": {
      "type": "object",
      "required": ["location", "header", "delimiter"],
      "properties": {
        "location": {
          "type": "array",
          "items": {
            "type": "string",
            "minItems": 1,
          },
          "message": {
            "required": "reference location not found",
            "type": "reference location item given is not a string",
          },
        },
        "header": {
          "type": "boolean",
          "message": {
            "required": "reference header not found",
            "type": "reference header given is not boolean",
          },
        },
        "delimiter": {
          "type": "string",
          "message": {
            "required": "reference delimiter not found",
            "type": "reference delimiter given is not a string",
          },
        },
      },
      "message": {
        "required": "reference array not found",
        "type": "reference array given is not an array",
      },
    },
    "lab": {
      "type": "object",
      "required": ["location", "header", "delimiter"],
      "properties": {
        "location": {
          "type": "array",
          "items": {
            "type": "string",
            "minItems": 1,
          },
          "message": {
            "required": "lab location not found",
            "type": "lab location item given is not a string",
          },
        },
        "header": {
          "type": "boolean",
          "message": {
            "required": "lab header not found",
            "type": "lab header given is not boolean",
          },
        },
        "delimiter": {
          "type": "string",
          "message": {
            "required": "lab delimiter not found",
            "type": "lab delimiter given is not a string",
          },
        },
      },
      "message": {
        "required": "reference array not found",
        "type": "reference array given is not an array",
      },
    },
    "schema": {
      "type": "array",
      "message": {
        "type": "schema given is not an array",
      },
    },
  },
};
