import {CarForm} from "../components/CarContainer/CarForm";
import {Cars} from "../components/CarContainer/Cars";
import {Chat} from "../components/CarContainer/Chat";

const CarPage = () => {
    return (
        <div>
            <CarForm/>
            <hr/>
            <Cars/>
            <hr/>
            <Chat/>
        </div>
    );
};

export {CarPage};