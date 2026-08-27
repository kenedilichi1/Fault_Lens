import dayjs from "dayjs";

export const getInitials = (name: string) => {
  return name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
};

export const timeFormatter = (date: Date) => {
  return dayjs(date).format("HH:mm:ss.SSS");
};