import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";


const PaperPlane = ({ shake }) => {
    return (
        <FontAwesomeIcon icon={faPaperPlane} 
        size="4X"/>
    );
};

export default PaperPlane;