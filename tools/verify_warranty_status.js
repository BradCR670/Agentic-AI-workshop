"use strict";

const MOCK_WARRANTY_LOOKUP = {
  GTW465ASNWW: {
    coverageMonths: 12,
    coverageType: "standard laundry coverage",
    notes: "Parts and labor are covered for the first year.",
  },
  GFW850SPNRS: {
    coverageMonths: 36,
    coverageType: "premium front-load washer coverage",
    notes: "Includes motor and drum coverage through the extended term.",
  },
  GSS25GYPFS: {
    coverageMonths: 24,
    coverageType: "refrigerator sealed-system coverage",
    notes: "Sealed-system components receive extra attention in service review.",
  },
  JGB735SPSS: {
    coverageMonths: 18,
    coverageType: "gas range limited coverage",
    notes: "Igniter and control-board diagnostics are prioritized.",
  },
  PDT715SYNFS: {
    coverageMonths: 30,
    coverageType: "dishwasher quiet-package coverage",
    notes: "Pump, rack, and leak-sensor claims are eligible during coverage.",
  },
};

const MS_PER_DAY = 24 * 60 * 60 * 1000;

function parseIsoDate(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);

  if (!match) {
    return null;
  }

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const parsedDate = new Date(year, month - 1, day);

  if (
    parsedDate.getFullYear() !== year ||
    parsedDate.getMonth() !== month - 1 ||
    parsedDate.getDate() !== day
  ) {
    return null;
  }

  return parsedDate;
}

function addMonthsClamped(date, monthsToAdd) {
  const monthIndex = date.getMonth() + monthsToAdd;
  const coverageYear = date.getFullYear() + Math.floor(monthIndex / 12);
  const coverageMonth = ((monthIndex % 12) + 12) % 12;
  const lastDayOfCoverageMonth = new Date(
    coverageYear,
    coverageMonth + 1,
    0,
  ).getDate();
  const coverageDay = Math.min(date.getDate(), lastDayOfCoverageMonth);

  return new Date(coverageYear, coverageMonth, coverageDay);
}

function startOfToday() {
  const now = new Date();

  return new Date(now.getFullYear(), now.getMonth(), now.getDate());
}

function verifyWarrantyStatus(modelName, purchaseDate) {
  const normalizedModel = String(modelName).trim().toUpperCase();
  const warrantyRecord = MOCK_WARRANTY_LOOKUP[normalizedModel];

  if (!warrantyRecord) {
    return {
      model_name: normalizedModel,
      status: "unknown_model",
      coverage_end_date: null,
      days_remaining: null,
      details: "No mock warranty rule is available for this model.",
    };
  }

  const purchasedOn = parseIsoDate(String(purchaseDate));

  if (!purchasedOn) {
    return {
      model_name: normalizedModel,
      status: "invalid_purchase_date",
      coverage_end_date: null,
      days_remaining: null,
      details: "Use YYYY-MM-DD format for purchase_date.",
    };
  }

  const coverageEnd = addMonthsClamped(
    purchasedOn,
    warrantyRecord.coverageMonths,
  );
  const daysRemaining = Math.round((coverageEnd - startOfToday()) / MS_PER_DAY);
  const status = daysRemaining >= 0 ? "active" : "expired";

  return {
    model_name: normalizedModel,
    status,
    coverage_end_date: coverageEnd.toISOString().slice(0, 10),
    days_remaining: Math.max(daysRemaining, 0),
    details: `${warrantyRecord.coverageType}: ${warrantyRecord.notes}`,
  };
}

module.exports = {
  verifyWarrantyStatus,
};
