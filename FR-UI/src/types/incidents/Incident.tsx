import { Associate } from "./Associate";
import { POI } from "./POI";
import { Suspect } from "./Suspect";

export default interface Incident {
    id: number;
    incidentId: string;
    dateTime: Date;
    accociates?: Associate[];
    suspects?: Suspect[];
    pois?: POI[];
    numberOfDetections: number;
    images: string[];
}


