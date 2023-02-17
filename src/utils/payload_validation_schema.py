payload_config_schema = {
  "type": "object",
  "required": ["reference", "lab", "results"],
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
        "folder": {
          "type": "boolean",
          "message": {
            "type": "reference folder given is not boolean",
          },
        },
        "type": {
          "type": "string",
          "enum":["txt","csv"],
          "message": {
            "type": "reference type given is not string",
            "enum": "reference type must be txt or csv",
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
        "folder": {
          "type": "boolean",
          "message": {
            "type": "lab folder given is not boolean",
          },
        },
        "type": {
          "type": "string",
          "enum":["txt","csv"],
          "message": {
            "type": "lab type given is not string",
            "enum": "lab type must be txt or csv",
          },
        },
      },
      "message": {
        "required": "reference array not found",
        "type": "reference array given is not an array",
      },
    },
    "results": {
      "type": "object",
      "required": ["location", "name", "type"],
      "properties": {
        "location": {
          "type": "array",
          "items": {
            "type": "string",
            "minItems": 1,
          },
          "message": {
            "required": "results location not found",
            "type": "results location item given is not a string",
          },
        },
        "name": {
          "type": "string",
          "message": {
            "required": "results name not found",
            "type": "results name given is not a string",
          },
        },
        "type": {
          "type": "string",
          "enum":["txt","csv"],
          "message": {
            "type": "results type given is not string",
            "enum": "results type must be txt or csv",
          },
        },
      },
      "message": {
        "required": "results array not found",
        "type": "results array given is not an array",
      },
    },
    "schema": {
      "type": "array",
      "message": {
        "type": "schema given is not an array",
      },
    },
    "error_margin": {
      "type": "integer",
      "message": {
        "type": "error_margin given is not an integer",
      },
    }
  },
};
