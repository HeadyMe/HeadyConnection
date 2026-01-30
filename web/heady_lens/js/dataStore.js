export const loadBodyPartData = async () => {
  const response = await fetch("./data/bodyParts.json");
  if (!response.ok) {
    throw new Error("Unable to load body part data.");
  }
  return response.json();
};

export const getPartInfo = (data, partKey) => data[partKey] ?? null;
